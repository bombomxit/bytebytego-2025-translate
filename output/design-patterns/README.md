# Design Patterns — Anh–Việt

[← Tủ sách · Bookshelf](../../README.md)

Cuốn sách gồm 23 mẫu thiết kế hướng đối tượng trong danh mục Gang of Four (GoF), với ví dụ TypeScript về tài liệu, workflow và tích hợp. Đọc từng chương để xem thay đổi cụ thể nào làm một mẫu trở nên hữu ích, chỗ nào trong mã chịu trách nhiệm và chi phí phải chấp nhận.

This book covers all 23 object-oriented Gang of Four (GoF) patterns through TypeScript examples from document management, workflows, and integrations. Each chapter shows the change that makes the pattern useful, where the responsibility belongs, and what the design costs.

## Bắt đầu đọc · Where to start

- Bắt đầu với [Strategy](vi/21-strategy.md) để thay một quy tắc, [Adapter](vi/06-adapter.md) để tích hợp một API và [Builder](vi/03-builder.md) để lắp ráp một đối tượng có ràng buộc.
- Start with [Strategy](original/21-strategy.md) to vary a rule, [Adapter](original/06-adapter.md) to integrate an API, and [Builder](original/03-builder.md) to assemble an object with construction constraints.
- Tra theo tình huống hoặc so sánh hai mẫu gần nhau trong [Hướng dẫn chọn mẫu](vi/24-chon-mau.md) · [Pattern selection guide](original/24-chon-mau.md).

## Mục lục

### Mẫu khởi tạo

| # | Mẫu | Dùng để làm gì và thường gặp ở đâu? | Bản Việt | Bản Anh |
| --- | --- | --- | --- | --- |
| 01 | Factory Method | Giao cho lớp con việc chọn loại đối tượng mà quy trình chung cần tạo.<br>Thường dùng khi cùng một luồng xuất dữ liệu phải hỗ trợ nhiều định dạng. | [Đọc](vi/01-factory-method.md) | [Đọc](original/01-factory-method.md) |
| 02 | Abstract Factory | Tạo một bộ thành phần tương thích để sử dụng cùng nhau.<br>Thường dùng khi đổi nhà cung cấp phải đổi cả bộ tích hợp. | [Đọc](vi/02-abstract-factory.md) | [Đọc](original/02-abstract-factory.md) |
| 03 | Builder | Tạo một đối tượng phức tạp qua nhiều bước cấu hình.<br>Thường dùng khi cấu hình báo cáo có nhiều tùy chọn và ràng buộc. | [Đọc](vi/03-builder.md) | [Đọc](original/03-builder.md) |
| 04 | Prototype | Tạo đối tượng mới từ một bản mẫu đã cấu hình.<br>Thường dùng khi nhân bản biểu mẫu hoặc quy trình để chỉnh sửa riêng. | [Đọc](vi/04-prototype.md) | [Đọc](original/04-prototype.md) |
| 05 | Singleton | Bảo đảm chỉ có một đối tượng thuộc một lớp trong phạm vi xác định.<br>Thường dùng khi một tiến trình cần đúng một đầu mối điều phối tài nguyên. | [Đọc](vi/05-singleton.md) | [Đọc](original/05-singleton.md) |

### Mẫu cấu trúc

| # | Mẫu | Dùng để làm gì và thường gặp ở đâu? | Bản Việt | Bản Anh |
| --- | --- | --- | --- | --- |
| 06 | Adapter | Chuyển giao diện của hệ thống bên ngoài sang giao diện ứng dụng cần.<br>Thường dùng khi tích hợp API mới hoặc thay nhà cung cấp. | [Đọc](vi/06-adapter.md) | [Đọc](original/06-adapter.md) |
| 07 | Bridge | Tách hai phần của thiết kế để chúng có thể thay đổi độc lập.<br>Thường dùng khi nhiều loại báo cáo phải hỗ trợ nhiều định dạng xuất. | [Đọc](vi/07-bridge.md) | [Đọc](original/07-bridge.md) |
| 08 | Composite | Cho phép thực hiện cùng một thao tác trên một phần tử hoặc cả nhóm lồng nhau.<br>Thường dùng khi làm việc với cây thư mục hoặc menu nhiều cấp. | [Đọc](vi/08-composite.md) | [Đọc](original/08-composite.md) |
| 09 | Decorator | Bọc một đối tượng để thêm hành vi và giữ nguyên cách gọi.<br>Thường dùng khi cần ghép các lớp ghi nhật ký, đo thời gian hoặc bộ nhớ đệm. | [Đọc](vi/09-decorator.md) | [Đọc](original/09-decorator.md) |
| 10 | Facade | Gom nhiều thao tác bên trong phân hệ thành một điểm gọi đơn giản.<br>Thường dùng khi nhiều nơi cần chạy chung một luồng, như xuất hồ sơ. | [Đọc](vi/10-facade.md) | [Đọc](original/10-facade.md) |
| 11 | Flyweight | Chia sẻ dữ liệu giống nhau giữa nhiều đối tượng để giảm bộ nhớ.<br>Thường dùng khi hiển thị nhiều nút sơ đồ có cùng kiểu trình bày. | [Đọc](vi/11-flyweight.md) | [Đọc](original/11-flyweight.md) |
| 12 | Proxy | Đặt một đối tượng đại diện để kiểm soát việc dùng đối tượng thật.<br>Thường dùng khi chỉ muốn tải tài nguyên nặng ở lần truy cập đầu tiên. | [Đọc](vi/12-proxy.md) | [Đọc](original/12-proxy.md) |

### Mẫu hành vi

| # | Mẫu | Dùng để làm gì và thường gặp ở đâu? | Bản Việt | Bản Anh |
| --- | --- | --- | --- | --- |
| 13 | Chain of Responsibility | Đưa yêu cầu qua một chuỗi bước có thể xử lý hoặc chuyển tiếp.<br>Thường dùng khi định tuyến hồ sơ theo nhiều quy tắc ưu tiên. | [Đọc](vi/13-chain-of-responsibility.md) | [Đọc](original/13-chain-of-responsibility.md) |
| 14 | Command | Đóng gói thao tác và dữ liệu cần thiết thành một lệnh để thực thi sau hoặc hoàn tác.<br>Thường dùng cho trình soạn thảo có nút hoàn tác hoặc tác vụ chạy nền. | [Đọc](vi/14-command.md) | [Đọc](original/14-command.md) |
| 15 | Interpreter | Đánh giá biểu thức theo các quy tắc của một ngôn ngữ nhỏ.<br>Thường dùng khi người dùng tự ghép điều kiện lọc tài liệu. | [Đọc](vi/15-interpreter.md) | [Đọc](original/15-interpreter.md) |
| 16 | Iterator | Duyệt từng phần tử qua một cách gọi chung mà không cần biết cách lưu trữ.<br>Thường dùng khi duyệt cây thư mục hoặc đọc dữ liệu phân trang. | [Đọc](vi/16-iterator.md) | [Đọc](original/16-iterator.md) |
| 17 | Mediator | Đưa quy tắc phối hợp vào một đầu mối để các thành phần ít phụ thuộc trực tiếp vào nhau.<br>Thường dùng khi nhiều trường trong một biểu mẫu cùng quyết định trạng thái nút gửi. | [Đọc](vi/17-mediator.md) | [Đọc](original/17-mediator.md) |
| 18 | Memento | Lưu và khôi phục trạng thái của đối tượng mà vẫn giữ kín cấu trúc bên trong.<br>Thường dùng khi cần quay lại một điểm đã lưu trong bản nháp hoặc sơ đồ. | [Đọc](vi/18-memento.md) | [Đọc](original/18-memento.md) |
| 19 | Observer | Thông báo sự kiện cho các thành phần đã đăng ký theo dõi.<br>Thường dùng khi một thay đổi cần làm mới nhiều phần của cùng một ứng dụng. | [Đọc](vi/19-observer.md) | [Đọc](original/19-observer.md) |
| 20 | State | Đổi hành vi và các bước chuyển hợp lệ theo trạng thái hiện tại.<br>Thường dùng trong vòng đời hồ sơ, đơn hàng hoặc yêu cầu phê duyệt. | [Đọc](vi/20-state.md) | [Đọc](original/20-state.md) |
| 21 | Strategy | Cho phép đổi cách tính hoặc quy tắc mà vẫn gọi theo cùng một cách.<br>Thường dùng khi phí vận chuyển, giảm giá hoặc thời gian xử lý có nhiều cách tính. | [Đọc](vi/21-strategy.md) | [Đọc](original/21-strategy.md) |
| 22 | Template Method | Giữ cố định trình tự chung và cho lớp con triển khai các bước được phép thay đổi.<br>Thường dùng khi nhiều loại dữ liệu đi qua cùng một quy trình nhập hoặc xuất. | [Đọc](vi/22-template-method.md) | [Đọc](original/22-template-method.md) |
| 23 | Visitor | Thêm thao tác cho nhiều loại phần tử đã hỗ trợ Visitor mà không sửa các lớp đó.<br>Thường dùng khi cần thêm báo cáo hoặc kiểm tra mới trên một cây dữ liệu có cấu trúc ổn định. | [Đọc](vi/23-visitor.md) | [Đọc](original/23-visitor.md) |

## Chạy ví dụ · Run an example

Chép khối TypeScript của một chương vào `example.ts` rồi chạy lệnh dưới đây. Mỗi ví dụ chạy độc lập, dùng cùng mã ở hai bản và sẽ báo lỗi nếu kết quả khác kỳ vọng.

Copy one chapter's TypeScript block into `example.ts` and run the command below. Each example is standalone, uses the same code in both editions, and throws if an expected result fails.

```sh
bun example.ts
```

## Biên soạn và nguồn · Editorial notes and sources

`original/` là bản Anh biên soạn cho tủ sách này, `vi/` là bản Việt tương ứng. Hai thư mục dùng cùng tên file. Nội dung và ví dụ TypeScript được viết riêng cho bộ sách dựa trên các khái niệm từ nguồn bên dưới.

`original/` contains the English text written for this bookshelf, and `vi/` contains the corresponding Vietnamese translation. Matching filenames identify chapter pairs. The prose and TypeScript examples were created for this book, with the sources below used as references.

- Erich Gamma, Richard Helm, Ralph Johnson và John Vlissides. [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610).
- Alexander Shvets. [Refactoring.Guru Design Patterns Catalog](https://refactoring.guru/design-patterns/catalog).
- Nguyễn Phúc. [Sách Design Pattern Tiếng Việt](https://github.com/nguyenphuc22/Design-Patterns).
