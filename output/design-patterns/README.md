# Design Patterns — Anh–Việt

[← Tủ sách · Bookshelf](../../README.md)

Cuốn sách gồm 23 mẫu thiết kế hướng đối tượng trong danh mục Gang of Four (GoF), với ví dụ TypeScript về tài liệu, workflow và tích hợp. Đọc từng chương để xem thay đổi cụ thể nào làm một mẫu trở nên hữu ích, chỗ nào trong mã chịu trách nhiệm và chi phí phải chấp nhận.

This book covers all 23 object-oriented Gang of Four (GoF) patterns through TypeScript examples from document management, workflows, and integrations. Each chapter shows the change that makes the pattern useful, where the responsibility belongs, and what the design costs.

## Bắt đầu đọc · Where to start

- Bắt đầu với [Strategy](vi/21-strategy.md) để thay một quy tắc, [Adapter](vi/06-adapter.md) để tích hợp một API và [Builder](vi/03-builder.md) để lắp ráp một đối tượng có ràng buộc.
- Start with [Strategy](original/21-strategy.md) to vary a rule, [Adapter](original/06-adapter.md) to integrate an API, and [Builder](original/03-builder.md) to assemble an object with construction constraints.
- Tra theo tình huống hoặc so sánh hai mẫu gần nhau trong [Hướng dẫn chọn mẫu](vi/24-chon-mau.md) · [Pattern selection guide](original/24-chon-mau.md).

## Mục lục · Contents

### Khởi tạo · Creational

| # | Mẫu · Pattern | Dùng để làm gì? · Purpose | Tiếng Việt | English |
| --- | --- | --- | --- | --- |
| 01 | Factory Method | Cho lớp con chọn đối tượng được tạo trong một quy trình có sẵn.<br>_Lets subclasses choose what an existing workflow creates._ | [Đọc](vi/01-factory-method.md) | [Read](original/01-factory-method.md) |
| 02 | Abstract Factory | Tạo một nhóm đối tượng liên quan có thể làm việc cùng nhau.<br>_Creates a family of related objects designed to work together._ | [Đọc](vi/02-abstract-factory.md) | [Read](original/02-abstract-factory.md) |
| 03 | Builder | Lắp ráp đối tượng phức tạp qua từng bước.<br>_Builds a complex object step by step._ | [Đọc](vi/03-builder.md) | [Read](original/03-builder.md) |
| 04 | Prototype | Tạo đối tượng mới bằng cách sao chép một mẫu đã cấu hình.<br>_Creates a new object by copying a configured prototype._ | [Đọc](vi/04-prototype.md) | [Read](original/04-prototype.md) |
| 05 | Singleton | Giữ đúng một instance của một lớp trong phạm vi đã định.<br>_Keeps one instance of a class within a defined scope._ | [Đọc](vi/05-singleton.md) | [Read](original/05-singleton.md) |

### Cấu trúc · Structural

| # | Mẫu · Pattern | Dùng để làm gì? · Purpose | Tiếng Việt | English |
| --- | --- | --- | --- | --- |
| 06 | Adapter | Chuyển interface của một API sang interface mà ứng dụng cần.<br>_Makes an API fit the interface the application expects._ | [Đọc](vi/06-adapter.md) | [Read](original/06-adapter.md) |
| 07 | Bridge | Tách hai phần để chúng thay đổi độc lập, ví dụ loại báo cáo và định dạng xuất.<br>_Lets two parts vary independently, such as report type and export format._ | [Đọc](vi/07-bridge.md) | [Read](original/07-bridge.md) |
| 08 | Composite | Xử lý từng phần tử và cả nhóm lồng nhau qua cùng một interface.<br>_Treats individual items and nested groups through one interface._ | [Đọc](vi/08-composite.md) | [Read](original/08-composite.md) |
| 09 | Decorator | Bọc đối tượng để thêm hành vi, chẳng hạn ghi log, mà vẫn giữ interface.<br>_Wraps an object to add behavior such as logging while preserving its interface._ | [Đọc](vi/09-decorator.md) | [Read](original/09-decorator.md) |
| 10 | Facade | Cung cấp một điểm gọi đơn giản cho một phân hệ phức tạp.<br>_Offers a simple entry point to a complex subsystem._ | [Đọc](vi/10-facade.md) | [Read](original/10-facade.md) |
| 11 | Flyweight | Giảm bộ nhớ bằng cách dùng chung dữ liệu lặp lại giữa nhiều đối tượng.<br>_Saves memory by sharing repeated data across many objects._ | [Đọc](vi/11-flyweight.md) | [Read](original/11-flyweight.md) |
| 12 | Proxy | Đứng thay đối tượng thật để kiểm soát truy cập hoặc trì hoãn khởi tạo.<br>_Stands in for an object to control access or defer creation._ | [Đọc](vi/12-proxy.md) | [Read](original/12-proxy.md) |

### Hành vi · Behavioral

| # | Mẫu · Pattern | Dùng để làm gì? · Purpose | Tiếng Việt | English |
| --- | --- | --- | --- | --- |
| 13 | Chain of Responsibility | Chuyển yêu cầu qua một chuỗi, nơi từng bước có thể xử lý hoặc chuyển tiếp.<br>_Passes a request along handlers that can handle it or forward it._ | [Đọc](vi/13-chain-of-responsibility.md) | [Read](original/13-chain-of-responsibility.md) |
| 14 | Command | Đóng gói một yêu cầu để có thể đưa vào hàng đợi hoặc hỗ trợ hoàn tác.<br>_Packages a request for queueing or undo._ | [Đọc](vi/14-command.md) | [Read](original/14-command.md) |
| 15 | Interpreter | Đánh giá biểu thức viết theo một ngữ pháp nhỏ, như quy tắc lọc tài liệu.<br>_Evaluates expressions in a small grammar, such as document filter rules._ | [Đọc](vi/15-interpreter.md) | [Read](original/15-interpreter.md) |
| 16 | Iterator | Duyệt từng phần tử mà không cần biết tập hợp lưu dữ liệu thế nào.<br>_Traverses a collection without exposing how it stores items._ | [Đọc](vi/16-iterator.md) | [Read](original/16-iterator.md) |
| 17 | Mediator | Tập trung việc phối hợp để các thành phần ít phụ thuộc trực tiếp vào nhau.<br>_Centralizes coordination so components depend less on one another._ | [Đọc](vi/17-mediator.md) | [Read](original/17-mediator.md) |
| 18 | Memento | Lưu và khôi phục trạng thái đối tượng mà vẫn giữ kín cấu trúc bên trong.<br>_Saves and restores an object's state without exposing its internals._ | [Đọc](vi/18-memento.md) | [Read](original/18-memento.md) |
| 19 | Observer | Thông báo thay đổi cho các thành phần đã đăng ký theo dõi.<br>_Notifies subscribed components when something changes._ | [Đọc](vi/19-observer.md) | [Read](original/19-observer.md) |
| 20 | State | Đổi hành vi và các bước chuyển hợp lệ theo trạng thái hiện tại.<br>_Varies behavior and allowed transitions with the current state._ | [Đọc](vi/20-state.md) | [Read](original/20-state.md) |
| 21 | Strategy | Cho phép thay quy tắc hoặc thuật toán mà vẫn dùng chung cách gọi.<br>_Makes rules or algorithms interchangeable behind one interface._ | [Đọc](vi/21-strategy.md) | [Read](original/21-strategy.md) |
| 22 | Template Method | Giữ trình tự xử lý chung và cho lớp con triển khai từng bước được định sẵn.<br>_Keeps a fixed workflow while subclasses implement selected steps._ | [Đọc](vi/22-template-method.md) | [Read](original/22-template-method.md) |
| 23 | Visitor | Thêm thao tác trên nhiều loại phần tử mà không sửa các lớp phần tử hiện có.<br>_Adds operations across element types without changing their existing classes._ | [Đọc](vi/23-visitor.md) | [Read](original/23-visitor.md) |

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
