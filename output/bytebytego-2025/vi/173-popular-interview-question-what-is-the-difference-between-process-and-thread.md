# 173 - Câu hỏi phỏng vấn phổ biến: Process và Thread khác nhau thế nào?

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 355-355
- Ảnh minh họa: `../assets/173/figure-01.png`

## Hình minh họa

![Popular interview question: What is the difference between Process and Thread?](../assets/173/figure-01.png)

## Dịch sát

Các khác biệt chính giữa process và thread:

- Process thường độc lập, trong khi thread tồn tại như các phần con của process.

- Mỗi process có memory space riêng. Các thread thuộc cùng một process chia sẻ cùng memory.

- Process là một operation nặng hơn. Việc tạo và kết thúc process mất nhiều thời gian hơn.

- Context switching giữa các process tốn kém hơn.

- Inter-thread communication nhanh hơn đối với thread.

## Dịch nội dung trong hình

- `Program (Disk)`: program là file/app nằm trên disk, ví dụ image capture app, movie app, UWP app, keynote app hoặc Microsoft Office app.
- `Process (RAM)`: khi program chạy, OS tạo process trong RAM. Task Manager hiển thị các process đang chạy, CPU, memory, disk, network và GPU usage.
- Luồng minh họa: `Program` nằm trên `Disk`, khi được chạy sẽ tạo ra một hoặc nhiều `Process` trong `RAM`.
- Bên trong process có `Thread`. Thread là execution path nhẹ hơn, chạy trong memory space của process.
- Một process có thể có nhiều thread; các thread trong cùng process chia sẻ memory nhưng có stack/execution context riêng.

## Tóm tắt & giải thích dễ hiểu

Process giống một ứng dụng đang chạy có vùng nhớ riêng. Thread giống các luồng công việc bên trong ứng dụng đó. Vì process tách memory nên an toàn hơn nhưng nặng hơn. Thread nhẹ và giao tiếp nhanh vì dùng chung memory, nhưng cũng dễ gây race condition nếu nhiều thread cùng sửa dữ liệu.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Chrome có thể chạy nhiều tab/site trong các process khác nhau để tăng isolation. Trong một backend service, một process Node.js hoặc Java có thể dùng nhiều thread hoặc worker để xử lý I/O, background job hoặc CPU-heavy task. Nếu một thread trong cùng process ghi sai dữ liệu shared state, bug có thể ảnh hưởng cả process.

## Thuật ngữ chính

- `Process`: instance của chương trình đang chạy, có memory space riêng.
- `Thread`: luồng thực thi bên trong process.
- `Memory space`: vùng nhớ mà process/thread truy cập.
- `Context switching`: chuyển CPU context giữa process/thread.
- `Inter-thread communication`: giao tiếp giữa các thread.
- `Race condition`: lỗi do nhiều luồng truy cập/sửa dữ liệu cùng lúc không kiểm soát.

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Suy ra từ tiêu đề/nội dung chính vì bài gốc không có câu hỏi riêng.

**Câu hỏi:** Popular interview question: What is the difference between Process and Thread?

**Trả lời:** Điểm khác nhau nên nhìn từ boundary và trách nhiệm chính. Với `Câu hỏi phỏng vấn phổ biến: Process và Thread khác nhau thế nào?`, hãy tách rõ mỗi bên giải quyết vấn đề gì, dữ liệu đi qua đâu, ai sở hữu state và lỗi sẽ lan như thế nào. Ý chính để giữ lại là: Process giống một ứng dụng đang chạy có vùng nhớ riêng. Thread giống các luồng công việc bên trong ứng dụng đó. Vì process tách memory nên an toàn hơn nhưng nặng hơn. Thread nhẹ và giao tiếp nhanh vì dùng chung memory, nhưng cũng dễ gây race condition nếu nhiều thread cùng sửa dữ liệu.

**Thinking học tập + liên hệ:** Khi so sánh trong `Câu hỏi phỏng vấn phổ biến: Process và Thread khác nhau thế nào?`, hãy tách responsibility, boundary, state, failure mode và cost vận hành thay vì chỉ so tên công nghệ. Lens chính là feedback loop, rollback, collaboration, code review và mức tự động hóa phù hợp team. Khi áp dụng vào team thật, hãy nhìn developer workflow như một hệ thống: commit, review, test, deploy và rollback đều phải giảm rủi ro production. Khi ghi chú lại, hãy giải thích được các keyword: `Process`, `Thread`, `Memory space`, `Context switching`, `Inter-thread communication`.
