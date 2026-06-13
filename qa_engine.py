"""
紧固件智能问答引擎
基于关键词匹配和语义理解的问答系统
"""
import re
from knowledge_base import FASTENER_KNOWLEDGE, QUICK_ANSWERS, WELCOME_MESSAGE


class FastenerQASystem:
    """紧固件问答系统"""

    def __init__(self):
        self.knowledge = FASTENER_KNOWLEDGE
        self.quick = QUICK_ANSWERS
        self.conversation_history = []

    def get_welcome(self):
        return WELCOME_MESSAGE

    def ask(self, question: str) -> str:
        """处理用户问题，返回答案"""
        q = question.strip().lower()
        if not q:
            return "请输入您的问题，我很乐意为您解答紧固件相关知识。"

        # 保存对话历史
        self.conversation_history.append({"role": "user", "content": question})

        # 1. 先检查快捷问答
        for key, answer in self.quick.items():
            if key in q or q in key:
                return answer

        # 2. 关键词匹配打分
        scored = []
        for topic_name, topic_data in self.knowledge.items():
            score = 0
            keywords = topic_data.get("keywords", [])
            for kw in keywords:
                if kw.lower() in q:
                    score += 1
            # 同时检查主题名是否匹配
            if topic_name.lower() in q:
                score += 2
            if score > 0:
                scored.append((score, topic_name, topic_data["answer"]))

        scored.sort(key=lambda x: x[0], reverse=True)

        # 3. 返回最佳匹配
        if scored:
            # 如果最高分明显高于其他，只返回一个
            if len(scored) == 1 or scored[0][0] > scored[1][0] * 1.5:
                answer = scored[0][2]
            else:
                # 返回多个相关主题
                parts = []
                for i, (score, name, ans) in enumerate(scored[:3]):
                    if score >= 1:
                        parts.append(f"### 📌 相关内容 {i+1}：{name}\n\n{ans}")
                answer = "\n\n---\n\n".join(parts) if parts else self._fallback(q)

            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer

        # 4. 智能兜底：分析问题意图
        answer = self._smart_fallback(q)
        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer

    def _smart_fallback(self, q: str) -> str:
        """智能兜底回答"""
        # 尝试匹配具体数字
        m = re.search(r'm(\d+)', q)
        if m:
            size = m.group(1)
            return f"""关于 **M{size}** 规格的紧固件：

**螺纹规格**：M{size}（公制粗牙螺纹）
**常见类型**：六角头螺栓 (GB/T 5782)、内六角圆柱头螺钉 (GB/T 70.1)、螺母 (GB/T 6170)

您想了解 M{size} 的哪方面信息呢？
• 螺纹螺距
• 拧紧扭矩
• 配用螺母规格
• 扳手尺寸

请告诉我具体想了解的内容，我会给您详细解答。"""

        # 匹配性能等级
        grade_match = re.search(r'(\d+\.?\d*)级', q)
        if grade_match:
            grade = grade_match.group(1)
            return f"关于 **{grade}级** 的性能等级，请参考性能等级相关知识。\n\n您可以尝试问：「8.8级和10.9级有什么区别？」"

        return self._fallback(q)

    def _fallback(self, q: str) -> str:
        """默认兜底"""
        return f"""关于「{q}」这个问题，我目前的知识库可能没有直接覆盖。

不过我可以帮您了解以下内容：
• 🔩 **紧固件类型**：螺栓、螺钉、螺母、垫圈、铆钉等
• 📐 **螺纹标准**：公制M螺纹、英制螺纹、螺距规格
• ⚙️ **性能等级**：4.8级、8.8级、10.9级、12.9级等
• 🛡️ **材料与表面处理**：碳钢、不锈钢、镀锌、达克罗等
• 🔧 **安装扭矩与防松**：拧紧力矩、防松措施
• ⚠️ **常见问题**：氢脆、咬死、滑丝、松动

请尝试换个方式提问，或者输入「帮助」查看示例问题。"""

    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
        return "对话历史已清除。"

    def get_suggestions(self) -> list:
        """获取推荐问题"""
        return [
            "螺栓和螺钉有什么区别？",
            "8.8级和10.9级螺栓有什么区别？",
            "M10螺栓的拧紧扭矩是多少？",
            "不锈钢螺栓有什么特点？",
            "弹簧垫圈怎么防松？",
            "什么是氢脆？如何预防？",
            "紧固件表面处理有哪些方式？",
            "粗牙螺纹和细牙螺纹怎么选？",
        ]


# 全局实例
qa_system = FastenerQASystem()
