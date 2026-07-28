# 167 - Các loại AI Agent

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 343-344
- Ảnh minh họa: `../assets/167/figure-01.png`

## Hình minh họa

![Types of AI Agents](../assets/167/figure-01.png)

## Dịch sát

AI agent không phải tất cả đều think và act theo cùng một cách. Chúng trải dài từ những system follow rule đơn giản tới system có thể learn và adapt. Mỗi loại đánh dấu một bước tiến trong cách machine perceive, decide và act.

1. Simple Reflex Agents: Chúng follow condition-action rule. Ví dụ, nếu temperature cao, bật fan. Không memory, không thinking, chỉ phản ứng tức thì. Chúng nhanh và đơn giản.

2. Model-based Reflex Agents: Chúng duy trì internal understanding về environment. Chúng không chỉ react với input ngay lập tức; chúng có một model giúp hiểu điều đang xảy ra ngoài những gì có thể thấy ngay bây giờ.

3. Goal-based Agents: Ở đây, focus chuyển sang goal. Decision được đưa ra dựa trên việc một action có đưa agent tiến gần hơn tới objective hay không.

4. Utility-based Agents: Chúng đi xa hơn bằng cách cân nhắc các outcome khác nhau. Chúng chọn action mang lại overall result tốt nhất, balance trade-off trên đường đi.

5. Learning Agents: Đây là loại advanced nhất. Chúng cải thiện liên tục, dùng feedback để adapt và perform tốt hơn theo thời gian.

## Dịch nội dung trong hình

- `Simple Reflex Agent`: sensor nhận environment, condition-action rule tạo action qua actuator.
- `Model-based Reflex Agent`: có model/internal state để interpret environment trước khi action.
- `Goal-based AI Agent`: dùng model/state và goal để ra decision-making path.
- `Utility-based AI Agent`: thêm utility function để cân nhắc outcome/trade-off.
- `Learning-based AI Agent`: có learning element, performance element, critic và problem generator để cải thiện qua feedback/outcome.

## Tóm tắt & giải thích dễ hiểu

Agent càng cao cấp càng có nhiều khả năng nội tại. Simple reflex chỉ phản ứng. Model-based có trạng thái/hiểu biết môi trường. Goal-based chọn hành động theo mục tiêu. Utility-based tối ưu kết quả theo điểm utility. Learning agent tự cải thiện qua feedback.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Thermostat bật/tắt theo nhiệt độ là simple reflex. Robot hút bụi nhớ bản đồ phòng là model-based. Agent tìm đường tới điểm đích là goal-based. Agent chọn route cân bằng thời gian, phí và rủi ro là utility-based. Agent học từ lần đi trước để chọn route tốt hơn là learning agent.

## Thuật ngữ chính

- `Agent`: thực thể quan sát và hành động.
- `Reflex agent`: agent phản xạ theo rule.
- `Internal model`: mô hình nội bộ về môi trường.
- `Goal`: mục tiêu cần đạt.
- `Utility`: điểm lợi ích/kết quả.
- `Feedback`: tín hiệu phản hồi.
- `Learning agent`: agent cải thiện qua kinh nghiệm.

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Suy ra từ tiêu đề/nội dung chính vì bài gốc không có câu hỏi riêng.

**Câu hỏi:** Sau khi đọc bài “Types of AI Agents”, ý chính cần trả lời và áp dụng vào system design là gì?

**Trả lời:** Sau bài này, phần đáng nhớ nhất là: Agent càng cao cấp càng có nhiều khả năng nội tại. Simple reflex chỉ phản ứng. Model-based có trạng thái/hiểu biết môi trường. Goal-based chọn hành động theo mục tiêu. Utility-based tối ưu kết quả theo điểm utility. Learning agent tự cải thiện qua feedback. Khi áp dụng vào hệ thống thật, hãy kiểm thêm quality, latency, cost/token, privacy, cập nhật tri thức và rủi ro hallucination.

**Thinking học tập + liên hệ:** Khi học `Các loại AI Agent`, hãy thử viết một checklist áp dụng vào project: input, output, owner, rủi ro và metric kiểm chứng. Lens chính là quality, latency, cost/token, privacy, cập nhật tri thức và rủi ro hallucination. Khi build AI app, hãy nối model với pipeline thật: data vào đâu, context lấy từ đâu, output được kiểm thế nào và chi phí tăng theo traffic ra sao. Khi ghi chú lại, hãy giải thích được các keyword: `Agent`, `Reflex agent`, `Internal model`, `Goal`, `Utility`.
