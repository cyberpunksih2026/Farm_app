import json
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List, Tuple
from app.core.config import settings

logger = logging.getLogger("farmapp.ai.ollama")


class OllamaClient:
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.AI_MODEL_NAME

    def check_health(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as res:
                return res.status == 200
        except Exception as e:
            logger.debug(f"Ollama health check failed: {e}")
            return False

    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Tuple[Optional[str], bool]:
        formatted_messages = []
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        formatted_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=15) as res:
                if res.status == 200:
                    resp_data = json.loads(res.read().decode("utf-8"))
                    content = resp_data.get("message", {}).get("content", "")
                    if content:
                        return content.strip(), False

        except Exception as exc:
            logger.warning(f"Ollama inference unavailable ({exc}). Using intelligent fallback engine.")

        last_prompt = messages[-1]["content"] if messages else "Hello"
        fallback_text = self._generate_heuristic_fallback(last_prompt)
        return fallback_text, True

    def _generate_heuristic_fallback(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "tomato" in prompt_lower:
            return (
                "🍅 **Farm Fresh Tomato Insights:**\n\n"
                "• **Varieties:** We have heirloom country tomatoes from Villupuram and Tindivanam FPO clusters.\n"
                "• **Storage Tip:** Store vine tomatoes at room temperature stem-down to preserve natural sweetness and aromatics.\n"
                "• **Transparency:** Farmers receive ~78% of the price (₹25–₹27/kg) compared to traditional wholesale markets."
            )
        elif "onion" in prompt_lower or "potato" in prompt_lower:
            return (
                "🥔 **Root Vegetables & Curing:**\n\n"
                "• **Organic Red Onions:** Naturally dried and cured in Cuddalore; packed with natural antioxidants.\n"
                "• **Golden Potatoes:** Freshly harvested thin-skinned tubers, ideal for curries, baking, and boiling without peeling.\n"
                "• **Storage Tip:** Store in a cool, well-ventilated dark bin. Keep onions and potatoes separated to prevent premature sprouting!"
            )
        elif "price" in prompt_lower or "transparency" in prompt_lower or "farmer" in prompt_lower:
            return (
                "🌱 **FarmApp Price Transparency Model:**\n\n"
                "At FarmApp, every product displays both the **Direct Farmer Payout** and the **Traditional Market Price**.\n"
                "Our direct FPO supply chain eliminates middleman compounding margins, ensuring farmers earn up to 80% more while consumers save 20-30%!"
            )
        elif "recipe" in prompt_lower or "cook" in prompt_lower or "dish" in prompt_lower:
            return (
                "🥗 **Farm Kitchen Recommendation - Country Tomato & Spinach Curry:**\n\n"
                "1. Sauté mustard seeds, curry leaves, and freshly sliced organic onions in cold-pressed oil.\n"
                "2. Add crushed garlic and chopped Villupuram country tomatoes with turmeric, coriander, and salt.\n"
                "3. Stir in freshly washed chopped Palak spinach and simmer for 5-7 minutes. Enjoy with steamed rice or hot rotis!"
            )
        else:
            return (
                "🌾 **Welcome to FarmApp Assistant!**\n\n"
                "I can help you explore our fresh harvest directly from verified smallholder farmers across Tamil Nadu & Puducherry.\n\n"
                "Ask me about:\n"
                "• Seasonal produce recommendations (tomatoes, greens, tubers, orchard fruits)\n"
                "• Farm-to-consumer price breakdowns\n"
                "• Crop storage tips and quick farm kitchen recipes!"
            )


ollama_client = OllamaClient()
