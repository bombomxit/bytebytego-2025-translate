# 101 - 5 Database Normal Form mọi developer nên biết

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 214-217
- Ảnh minh họa: `../assets/101/figure-01.png`, `../assets/101/figure-02.png`

## Hình minh họa

![5 Database Normal Forms Every Developer Should Know](../assets/101/figure-01.png)

![Best Ways to Test System Functionality](../assets/101/figure-02.png)

## Dịch sát

Normalization nhằm loại bỏ redundancy và enforce data integrity bằng cách tổ chức data thành các form logic, dựa trên dependency.

1. First Normal Form (1NF): Loại bỏ repeating group và bảo đảm atomic value trong mỗi column.

2. Second Normal Form (2NF): Loại bỏ partial dependency bằng cách bảo đảm tất cả non-key column phụ thuộc vào toàn bộ primary key.

3. Third Normal Form (3NF): Loại bỏ transitive dependency, bảo đảm non-key column chỉ phụ thuộc vào primary key.

4. Boyce-Codd Normal Form (BCNF): Tăng cường 3NF bằng cách loại bỏ anomaly tồn tại do overlapping candidate key. Nếu một column phụ thuộc vào một column khác, thì “column khác” đó phải đủ để identify duy nhất từng row.

5. Fourth Normal Form (4NF): Bảo đảm một table không trộn nhiều independent one-to-many relationship cho cùng một entity.

Câu hỏi dành cho bạn: Bạn sẽ thêm Normal Form nào khác vào danh sách?

Best ways to test system functionality

Testing system functionality là bước quan trọng trong software development và engineering process.

Nó bảo đảm system hoặc software application hoạt động như kỳ vọng, đáp ứng user requirement và vận hành reliable.

Dưới đây là các cách tốt nhất:

1. Unit Testing: Bảo đảm từng code component riêng lẻ hoạt động đúng khi isolation.

2. Integration Testing: Verify các phần khác nhau của system hoạt động mượt mà cùng nhau.

3. System Testing: Đánh giá toàn bộ system có tuân thủ user requirement và performance hay không.

4. Load Testing: Test khả năng system xử lý high workload và xác định performance issue.

5. Error Testing: Đánh giá cách software xử lý invalid input và error condition.

6. Test Automation: Tự động hóa test case execution để tăng efficiency, repeatability và giảm lỗi.

Câu hỏi dành cho bạn: Bạn approach testing system functionality trong software development hoặc engineering project của mình như thế nào?

Câu hỏi dành cho bạn: Release process của công ty bạn trông như thế nào?

## Dịch nội dung trong hình

- Hình 1: minh họa 1NF tách repeating/atomic value, 2NF tách partial dependency, 3NF tách transitive dependency, BCNF xử lý candidate key overlap và 4NF tách multiple independent relationships.
- Hình 2: testing functionality gồm process và tool: Unit Testing, Integration Testing, System Testing, Load Testing, Error Testing và Test Automation.
- Tool trong hình gồm pytest, JUnit, QUnit, Postman, SoapUI, Selenium/Cucumber/Appium, JMeter/Gatling/Locust, Gremlin, Jenkins, Travis CI, CircleCI và GitHub Actions.

## Tóm tắt & giải thích dễ hiểu

Normalization giúp schema ít trùng lặp và giảm anomaly khi insert/update/delete. 1NF xử lý atomicity, 2NF xử lý phụ thuộc vào một phần composite key, 3NF xử lý phụ thuộc bắc cầu, BCNF siết chặt candidate key, 4NF xử lý nhiều quan hệ một-nhiều độc lập trong cùng bảng.

Phần testing trong cùng file nhấn mạnh hệ thống không chỉ cần code đúng từng function mà còn cần kiểm tra tích hợp, toàn hệ thống, tải cao, lỗi bất thường và tự động hóa để release ổn định.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Nếu bảng `orders` lưu cả `customer_name`, `customer_email`, `product_name`, `product_category` lặp lại ở nhiều row, update email hoặc category dễ bị lệch. Normalization tách `customers`, `products`, `orders`, `order_items` để mỗi fact có một nơi lưu chính. Sau đó test pipeline cần unit test price calculation, integration test checkout/payment, load test flash sale và error test payment gateway timeout.

## Thuật ngữ chính

- `Normalization`: chuẩn hóa schema để giảm redundancy.
- `Redundancy`: dữ liệu trùng lặp.
- `Atomic value`: giá trị không chia nhỏ thêm trong column.
- `Partial dependency`: phụ thuộc vào một phần khóa ghép.
- `Transitive dependency`: phụ thuộc bắc cầu qua non-key column.
- `Candidate key`: khóa ứng viên xác định row duy nhất.
- `Load testing`: kiểm tra dưới tải cao.

