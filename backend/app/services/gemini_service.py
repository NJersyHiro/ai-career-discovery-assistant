import json
import re
from typing import Dict, Any, Optional, List
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for interacting with Google Gemini API for career analysis."""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def analyze_resume(self, resume_text: str, document_type: str) -> Dict[str, Any]:
        """Analyze resume/CV using Gemini API."""
        
        prompt = self._create_analysis_prompt(resume_text, document_type)
        
        try:
            # Generate content using Gemini
            response = await self.model.generate_content_async(prompt)
            
            if not response.text:
                logger.error("No text in Gemini response")
                raise ValueError("Gemini returned empty response")
            
            logger.info(f"Raw Gemini response length: {len(response.text)}")
            
            # Extract JSON from response
            parsed_response = self._extract_json_from_response(response.text)
            
            return {
                "success": True,
                "data": parsed_response,
                "raw_response": response.text
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def analyze_resume_sync(self, resume_text: str, document_type: str) -> Dict[str, Any]:
        """Synchronous version of analyze_resume for Celery tasks."""
        
        prompt = self._create_analysis_prompt(resume_text, document_type)
        
        try:
            # Generate content using Gemini (synchronous)
            response = self.model.generate_content(prompt)
            
            if not response.text:
                logger.error("No text in Gemini response")
                raise ValueError("Gemini returned empty response")
            
            logger.info(f"Raw Gemini response length: {len(response.text)}")
            
            # Extract JSON from response
            parsed_response = self._extract_json_from_response(response.text)
            
            return {
                "success": True,
                "data": parsed_response,
                "raw_response": response.text
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, resume_text: str, document_type: str) -> str:
        """Create prompt for Gemini based on document type."""
        
        doc_type_name = "履歴書" if document_type == "resume" else "職務経歴書"
        
        return f"""
あなたはキャリアアドバイザーAIです。以下の{doc_type_name}を分析し、キャリアパスの提案を行ってください。

分析する内容:
1. スキルと経験の抽出
2. 3つのキャリアパス提案（企業転職、フリーランス、起業）
3. 各パスに必要なスキルと、既存スキルとのマッチ度計算
4. 各パスに必要なスキルギャップ
5. 推定年収レンジ（日本市場）
6. 具体的な次のステップ

重要: skill_match_percentageは、候補者の現在のスキルが各キャリアパスに必要なスキルとどの程度マッチしているかを0-100の整数で必ず計算してください。

以下の形式の厳密なJSONのみを出力してください（JSON以外の解説文、マークダウン、``` などを絶対に含めないでください）:

{{
  "extracted_skills": ["スキル1", "スキル2", ...],
  "experience_summary": "経験の要約",
  "career_paths": [
    {{
      "type": "corporate",
      "title": "職種名",
      "description": "説明",
      "required_skills": ["必要スキル1", ...],
      "skill_match_percentage": スキルマッチ度(0-100の整数),
      "skill_gaps": ["不足スキル1", ...],
      "salary_range": {{
        "min": 最低年収(整数),
        "max": 最高年収(整数)
      }},
      "market_demand": "high/medium/low",
      "confidence_score": 0.0-1.0の小数,
      "next_steps": ["ステップ1", ...]
    }},
    {{
      "type": "freelance",
      ...同様の構造
    }},
    {{
      "type": "entrepreneurship",
      ...同様の構造
    }}
  ],
  "overall_insights": "全体的な洞察"
}}

{doc_type_name}の内容:
\"\"\"
{resume_text}
\"\"\"
"""
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON object from Gemini response text."""
        
        # Try to find JSON object in response
        match = re.search(r'\{[\s\S]*\}', response_text)
        
        if not match:
            logger.error("No JSON found in response")
            raise ValueError("No valid JSON format found in response")
        
        json_text = match.group(0)
        
        try:
            parsed = json.loads(json_text)
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            raise ValueError(f"Invalid JSON format: {str(e)}")
    
    async def generate_detailed_career_path(
        self,
        career_type: str,
        skills: List[str],
        experience: str
    ) -> Dict[str, Any]:
        """Generate detailed career path recommendations."""
        
        prompt = f"""
以下の情報を基に、{career_type}のキャリアパスの詳細な分析を提供してください。

現在のスキル: {', '.join(skills)}
経験: {experience}

以下の形式の厳密なJSONのみを出力してください:

{{
  "detailed_path": {{
    "title": "具体的な職種/ビジネス名",
    "description": "詳細な説明",
    "pros": ["メリット1", ...],
    "cons": ["デメリット1", ...],
    "required_skills": ["必須スキル1", ...],
    "recommended_courses": [
      {{
        "name": "コース名",
        "platform": "プラットフォーム",
        "duration": "期間",
        "cost": "費用"
      }}
    ],
    "estimated_preparation_time": 準備期間（週）,
    "success_stories": ["成功事例1", ...],
    "market_trends": "市場トレンド分析"
  }}
}}
"""
        
        try:
            response = await self.model.generate_content_async(prompt)
            parsed_response = self._extract_json_from_response(response.text)
            return parsed_response
        except Exception as e:
            logger.error(f"Detailed path generation error: {str(e)}")
            raise


# Singleton instance
gemini_service = GeminiService()