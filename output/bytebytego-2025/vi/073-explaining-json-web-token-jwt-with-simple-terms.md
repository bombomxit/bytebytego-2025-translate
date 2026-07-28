# 073 - Giải thích JSON Web Token (JWT) bằng ngôn ngữ đơn giản

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 156-157
- Ảnh minh họa: `../assets/073/figure-01.png`

## Hình minh họa

![JSON Web Token explained](../assets/073/figure-01.png)

## Dịch sát

Hãy tưởng tượng bạn có một chiếc hộp đặc biệt gọi là JWT. Bên trong chiếc hộp này có ba phần: header, payload và signature.

Header giống như nhãn dán bên ngoài hộp. Nó cho chúng ta biết đây là loại hộp gì và nó được bảo vệ bằng cách nào. Header thường được viết ở format gọi là JSON, tức là một cách tổ chức thông tin bằng dấu ngoặc nhọn `{ }` và dấu hai chấm `:`.

Payload giống như thông điệp hoặc thông tin thật sự mà bạn muốn gửi. Nó có thể là tên, tuổi hoặc bất kỳ dữ liệu nào bạn muốn chia sẻ. Payload cũng được viết ở JSON format, nên dễ hiểu và dễ xử lý.

Signature là phần làm cho JWT an toàn. Nó giống như một con dấu đặc biệt mà chỉ người gửi biết cách tạo. Signature được tạo bằng một secret code, gần giống như password. Signature này đảm bảo rằng không ai có thể chỉnh sửa nội dung JWT mà người gửi không biết.

Khi bạn muốn gửi JWT tới server, bạn đặt header, payload và signature vào trong chiếc hộp. Sau đó bạn gửi nó tới server. Server có thể dễ dàng đọc header và payload để hiểu bạn là ai và bạn muốn làm gì.

Câu hỏi dành cho bạn: Khi nào chúng ta nên dùng JWT cho authentication? Có những phương pháp authentication nào khác?

## Dịch nội dung trong hình

- JWT là viết tắt của `JSON Web Token`.
- JSON là file/data format đơn giản để lưu dữ liệu theo cặp key-value, ví dụ `"what": "JSON"`.
- JWT structure gồm 3 phần: `header.payload.signature`, thường được biểu diễn thành chuỗi dạng `x.y.z` sau khi base64 encode.
- Luồng hoạt động cơ bản: user login, server validate credential, server trả JWT, client lưu JWT, rồi gửi JWT trong request sau để server kiểm tra.
- Phần signing có thể dùng public/private key hoặc symmetric key để tạo và verify chữ ký.

## Tóm tắt & giải thích dễ hiểu

JWT là một token có cấu trúc rõ ràng, thường dùng để truyền thông tin đã được ký giữa client và server. Header mô tả thuật toán ký, payload chứa claim/dữ liệu, signature giúp server kiểm tra token có bị sửa hay không.

Điểm dễ nhầm: payload của JWT thường chỉ được encode, không nhất thiết được encrypt. Nghĩa là người khác có thể đọc nội dung payload nếu có token. Vì vậy không nên đưa password, secret, số thẻ hoặc dữ liệu nhạy cảm vào payload.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Khi user login vào app, server có thể trả access token dạng JWT chứa `user_id`, `role` và `exp`. Mỗi request sau đó gửi header `Authorization: Bearer <token>`. API Gateway hoặc backend verify signature và expiration trước khi cho truy cập resource.

JWT phù hợp khi cần stateless authentication giữa nhiều service. Nhưng nếu muốn revoke token ngay lập tức, ví dụ user bị khóa tài khoản, hệ thống cần thêm blacklist, short-lived token hoặc introspection endpoint.

## Thuật ngữ chính

- `JWT`: JSON Web Token.
- `Header`: phần mô tả metadata và thuật toán ký token.
- `Payload`: phần chứa claims/dữ liệu.
- `Signature`: chữ ký để phát hiện token bị sửa.
- `Claim`: thông tin được khai báo trong payload.
- `Base64URL`: kiểu encode thường dùng trong JWT.
- `Authentication`: xác thực danh tính người dùng.

