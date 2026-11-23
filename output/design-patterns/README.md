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

| # | Mẫu · Pattern | Tiếng Việt | English |
| --- | --- | --- | --- |
| 01 | Factory Method | [Đọc](vi/01-factory-method.md) | [Read](original/01-factory-method.md) |
| 02 | Abstract Factory | [Đọc](vi/02-abstract-factory.md) | [Read](original/02-abstract-factory.md) |
| 03 | Builder | [Đọc](vi/03-builder.md) | [Read](original/03-builder.md) |
| 04 | Prototype | [Đọc](vi/04-prototype.md) | [Read](original/04-prototype.md) |
| 05 | Singleton | [Đọc](vi/05-singleton.md) | [Read](original/05-singleton.md) |

### Cấu trúc · Structural

| # | Mẫu · Pattern | Tiếng Việt | English |
| --- | --- | --- | --- |
| 06 | Adapter | [Đọc](vi/06-adapter.md) | [Read](original/06-adapter.md) |
| 07 | Bridge | [Đọc](vi/07-bridge.md) | [Read](original/07-bridge.md) |
| 08 | Composite | [Đọc](vi/08-composite.md) | [Read](original/08-composite.md) |
| 09 | Decorator | [Đọc](vi/09-decorator.md) | [Read](original/09-decorator.md) |
| 10 | Facade | [Đọc](vi/10-facade.md) | [Read](original/10-facade.md) |
| 11 | Flyweight | [Đọc](vi/11-flyweight.md) | [Read](original/11-flyweight.md) |
| 12 | Proxy | [Đọc](vi/12-proxy.md) | [Read](original/12-proxy.md) |

### Hành vi · Behavioral

| # | Mẫu · Pattern | Tiếng Việt | English |
| --- | --- | --- | --- |
| 13 | Chain of Responsibility | [Đọc](vi/13-chain-of-responsibility.md) | [Read](original/13-chain-of-responsibility.md) |
| 14 | Command | [Đọc](vi/14-command.md) | [Read](original/14-command.md) |
| 15 | Interpreter | [Đọc](vi/15-interpreter.md) | [Read](original/15-interpreter.md) |
| 16 | Iterator | [Đọc](vi/16-iterator.md) | [Read](original/16-iterator.md) |
| 17 | Mediator | [Đọc](vi/17-mediator.md) | [Read](original/17-mediator.md) |
| 18 | Memento | [Đọc](vi/18-memento.md) | [Read](original/18-memento.md) |
| 19 | Observer | [Đọc](vi/19-observer.md) | [Read](original/19-observer.md) |
| 20 | State | [Đọc](vi/20-state.md) | [Read](original/20-state.md) |
| 21 | Strategy | [Đọc](vi/21-strategy.md) | [Read](original/21-strategy.md) |
| 22 | Template Method | [Đọc](vi/22-template-method.md) | [Read](original/22-template-method.md) |
| 23 | Visitor | [Đọc](vi/23-visitor.md) | [Read](original/23-visitor.md) |

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
