# Cách chọn mẫu thiết kế

[Mục lục](../README.md) · [English](../original/24-chon-mau.md)

## Bắt đầu từ thay đổi cụ thể

1. Nêu một thay đổi đã gặp hoặc sắp gặp. Ví dụ, “nhà cung cấp preview thứ hai trả kết quả với cấu trúc khác” đủ cụ thể để trao đổi.
2. Xác định nơi chịu trách nhiệm xử lý thay đổi. Với nhà cung cấp preview, đặt phần chuyển đổi ở ranh giới tích hợp và định nghĩa kiểu kết quả mà phần còn lại của ứng dụng cần.
3. Thử thiết kế nhỏ nhất đáp ứng nhu cầu. Với một nhà cung cấp, một hàm ánh xạ có thể đủ. Tách adapter khi nhiều triển khai thực sự cần tuân theo cùng một hợp đồng.
4. Kiểm chứng thay đổi kế tiếp. Thêm một biến thể mới rồi xem phải sửa những file nào, kiểm thử hợp đồng nào vẫn qua và tình huống lỗi mới nào cần kiểm thử.

## Tra mẫu theo tình huống

Tìm tình huống gần với bài toán của mình rồi đọc phần giải pháp đơn giản hơn và phần đánh đổi của chương tương ứng.

| Tình huống | Mẫu thiết kế |
| --- | --- |
| Một luồng có sẵn cần cho lớp con chọn thành phần mà luồng khởi tạo. | [Factory Method](01-factory-method.md) |
| Các thành phần cùng nhà cung cấp cần tương thích với nhau. | [Abstract Factory](02-abstract-factory.md) |
| Đối tượng cần lắp ráp qua nhiều bước và chỉ có một số tổ hợp hợp lệ. | [Builder](03-builder.md) |
| Cần lấy một đối tượng đã cấu hình làm mẫu cho các bản sao độc lập. | [Prototype](04-prototype.md) |
| Một phạm vi chạy xác định chỉ được phép có một đối tượng sở hữu tài nguyên. | [Singleton](05-singleton.md) |
| Một API mà ứng dụng không thể sửa cần đáp ứng interface nội bộ. | [Adapter](06-adapter.md) |
| Hai chiều biến đổi của một thành phần cần phát triển độc lập. | [Bridge](07-bridge.md) |
| Node lá và cây con cần hỗ trợ cùng một thao tác. | [Composite](08-composite.md) |
| Nhiều trách nhiệm tùy chọn cần bọc quanh cùng một thao tác lõi. | [Decorator](09-decorator.md) |
| Bên gọi cần một điểm vào ổn định cho một phân hệ nhiều bước. | [Facade](10-facade.md) |
| Nhiều đối tượng lặp lại cùng một phần dữ liệu nội tại có thể dùng chung. | [Flyweight](11-flyweight.md) |
| Cần đối tượng đại diện kiểm soát thời điểm truy cập đối tượng thật. | [Proxy](12-proxy.md) |
| Một chuỗi xử lý có thứ tự có thể tiếp nhận, chuyển tiếp hoặc dừng yêu cầu. | [Chain of Responsibility](13-chain-of-responsibility.md) |
| Cần biểu diễn thao tác thành một giá trị để thực thi sau. | [Command](14-command.md) |
| Các quy tắc nghiệp vụ có thể kết hợp theo một văn phạm nhỏ. | [Interpreter](15-interpreter.md) |
| Bên gọi cần duyệt tập hợp mà không phụ thuộc vào cách nó lưu dữ liệu. | [Iterator](16-iterator.md) |
| Một nhóm thành phần cần một nơi quản lý quy tắc phối hợp. | [Mediator](17-mediator.md) |
| Cần khôi phục trạng thái cũ mà vẫn giữ tính đóng gói của đối tượng. | [Memento](18-memento.md) |
| Một thay đổi trong cùng tiến trình cần báo cho nhiều bên lắng nghe độc lập. | [Observer](19-observer.md) |
| Giai đoạn vòng đời quyết định thao tác nào hợp lệ và được chuyển sang trạng thái nào. | [State](20-state.md) |
| Bên gọi chọn một trong nhiều thuật toán có cùng hợp đồng. | [Strategy](21-strategy.md) |
| Các lớp con thay đổi từng bước trong một quy trình kế thừa chung. | [Template Method](22-template-method.md) |
| Mô hình phần tử ổn định nhưng thường xuyên có thêm thao tác. | [Visitor](23-visitor.md) |

## Phân biệt các mẫu gần nhau

- **Strategy và State.** Bên gọi truyền Strategy cho một phép tính hoặc chính sách. State thể hiện một giai đoạn trong vòng đời đối tượng, quyết định thao tác nào hợp lệ và có thể chuyển sang giai đoạn nào.
- **Adapter, Facade và Bridge.** Adapter chuyển đổi interface bên ngoài sang interface bên gọi cần. Facade cho bên gọi một điểm vào ở mức cao hơn để dùng một phân hệ. Bridge tách hai chiều biến đổi cần phát triển độc lập.
- **Decorator và Proxy.** Decorator thêm trách nhiệm có thể kết hợp qua nhiều lớp bọc mà vẫn giữ interface. Proxy đứng thay cho đối tượng thật và có thể quyết định chuyển tiếp như thế nào hoặc khi nào.
- **Factory Method, Abstract Factory và Builder.** Factory Method cho lớp con ghi đè bước khởi tạo. Abstract Factory tạo một họ sản phẩm tương thích. Builder lắp ráp một sản phẩm qua nhiều bước.
- **Observer và publish–subscribe.** Ví dụ Observer gọi listener trong cùng tiến trình. Khi đi qua ranh giới dịch vụ, thiết kế cần tính đến broker, bảo đảm chuyển giao, idempotency và cách xử lý lỗi.
- **Strategy và Template Method.** Strategy giao một quy tắc cho thành phần mà bên gọi truyền vào. Template Method dùng kế thừa để lớp con triển khai các bước đã định trong quy trình của lớp cơ sở.
- **Command và Memento.** Command lưu thông tin về thao tác cần thực thi. Memento lưu trạng thái của một đối tượng tại một thời điểm. Tính năng hoàn tác có thể dùng command đảo ngược được, memento hoặc kết hợp cả hai.

## Thuật ngữ

| Thuật ngữ | English | Nghĩa trong sách |
| --- | --- | --- |
| Kết hợp đối tượng | Composition | Đối tượng giao việc cho thành phần cộng tác mà nó giữ hoặc nhận vào. |
| Kế thừa | Inheritance | Lớp con chuyên biệt hóa kiểu cơ sở và có thể kế thừa phần triển khai. |
| Hợp đồng | Contract | Hành vi mà bên gọi có thể dựa vào, gồm đầu vào, đầu ra, lỗi và tác dụng phụ. |
| Ranh giới | Boundary | Điểm chuyển giao trách nhiệm hoặc sự phụ thuộc. |
| Vòng đời | Lifecycle | Các giai đoạn một đối tượng có thể đi qua và thời điểm tạo hoặc giải phóng tài nguyên. |
| Bất biến | Invariant | Quy tắc phải đúng trong mọi trạng thái hợp lệ. |

[← Chương trước · 23. Visitor](23-visitor.md)
