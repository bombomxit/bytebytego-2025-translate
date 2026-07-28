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

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Câu hỏi trong tài liệu gốc.

**Câu hỏi:** Khi nào chúng ta nên dùng JWT cho authentication?

**Trả lời:** Nên dùng JWT khi hệ thống cần stateless authentication cho API/mobile/SPA, có nhiều backend service cùng verify token, traffic cao và chấp nhận mô hình access token ngắn hạn. Không nên dùng JWT như session dài hạn nếu cần revoke tức thì, kiểm soát trạng thái đăng nhập chặt hoặc lưu dữ liệu nhạy cảm trong token. Trong các case đó, server-side session, token introspection hoặc access token ngắn hạn + refresh token sẽ an toàn/dễ kiểm soát hơn.

**Thinking học tập + liên hệ:** Quyết định trong `Giải thích JSON Web Token (JWT) bằng ngôn ngữ đơn giản` chỉ có ý nghĩa khi nêu được điều kiện dùng, điều kiện không dùng và tín hiệu nào chứng minh lựa chọn đang đúng. Lens chính là actor, trust boundary, dữ liệu nhạy cảm, lifetime của token/key, quyền truy cập và cơ chế revoke. Khi làm API thật, một endpoint chạy được chưa đủ; phải kiểm thêm abuse, audit log, error leakage, rate limit và quyền ở service chứa dữ liệu. Khi ghi chú lại, hãy giải thích được các keyword: `JWT`, `Header`, `Payload`, `Signature`, `Claim`.

### Câu hỏi 2

**Nguồn câu hỏi:** Câu hỏi trong tài liệu gốc.

**Câu hỏi:** Có những phương pháp authentication nào khác?

**Trả lời:** Ngoài JWT, các lựa chọn authentication/authentication-related phổ biến gồm server-side session bằng cookie, OAuth2/OIDC cho đăng nhập qua identity provider, SSO cho doanh nghiệp, API key cho machine-to-machine đơn giản, mTLS cho service nội bộ cần xác thực hai chiều, WebAuthn/passkey cho login chống phishing và PASETO nếu muốn token có mặc định crypto an toàn hơn JWT. Chọn cách nào phụ thuộc client là browser/mobile/service, yêu cầu revoke, mức nhạy cảm dữ liệu và khả năng vận hành key/session store.

**Thinking học tập + liên hệ:** Khi bài hỏi còn thiếu gì trong `Giải thích JSON Web Token (JWT) bằng ngôn ngữ đơn giản`, hãy so danh sách hiện tại với nhu cầu production: scale, debug, security, cost và vận hành. Lens chính là actor, trust boundary, dữ liệu nhạy cảm, lifetime của token/key, quyền truy cập và cơ chế revoke. Khi làm API thật, một endpoint chạy được chưa đủ; phải kiểm thêm abuse, audit log, error leakage, rate limit và quyền ở service chứa dữ liệu. Khi ghi chú lại, hãy giải thích được các keyword: `JWT`, `Header`, `Payload`, `Signature`, `Claim`.
