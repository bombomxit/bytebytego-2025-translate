# Design Doc: Sharing 1 tiếng về request, cache, Redis và database

## 1. Bối cảnh

Bố Toàn đã đăng ký một buổi sharing 1 tiếng cho team dev gồm backend, frontend và mobile. Chủ đề đăng ký ban đầu là:

- `khác biệt giữa Redis và database`
- `tối ưu truy vấn khi sử dụng index trong database`

Vấn đề hiện tại là nếu giữ đúng hai nhánh này làm trục chính thì buổi chia sẻ dễ bị lệch quá nhiều về backend, trong khi audience là mixed team và mục tiêu mong muốn là có góc nhìn toàn cảnh hơn.

Hướng chốt cho buổi này là:

- Lấy `một request chậm đi qua hệ thống như thế nào` làm trục kể chuyện.
- Redis và index chỉ là hai điểm dừng quan trọng trong hành trình đó.
- Dùng mental model `RAM vs ổ cứng`, `cache vs source of truth`, `index vs full scan` để giúp người nghe không backend cũng theo được.

## 2. Audience và mức độ

Audience:

- Backend developers
- Frontend developers
- Mobile developers

Mức độ:

- `Cân bằng`
- Ưu tiên dễ hiểu, có liên hệ thực tế
- Có một vài đoạn đào sâu vừa đủ về Redis, memory, disk, query path và index
- Không biến buổi này thành bài giảng thuần database internals

## 3. Mục tiêu buổi sharing

Sau buổi này, người nghe nên nắm được 3 ý chính:

1. Khi app/web chậm, độ trễ có thể nằm ở nhiều lớp chứ không chỉ ở database.
2. Redis nhanh không phải vì “xịn hơn database”, mà vì nó giải một bài toán khác trên memory và thường không phải source of truth.
3. Index giúp database đọc nhanh hơn bằng cách thêm cấu trúc tra cứu, nhưng nó không miễn phí và không thay thế cho việc hiểu query pattern.

## 4. Anti-goals

Buổi sharing này không cố làm các việc sau:

- Dạy chi tiết toàn bộ persistence model của Redis
- Dạy thiết kế index chuyên sâu cho từng loại database engine
- So sánh benchmark Redis với PostgreSQL/MySQL theo số liệu cụ thể
- Đi sâu vào tuning production như vacuum, checkpoint, fsync policy, lock escalation

Những phần đó có thể nhắc đến như câu hỏi mở hoặc optional appendix, nhưng không được chiếm trục chính.

## 5. Thông điệp cốt lõi

Các câu nên được lặp lại trong suốt buổi:

- `Cache không chỉ là Redis.`
- `Một request đi qua nhiều tầng, và mỗi tầng đều có thể là bottleneck.`
- `Redis thường là lớp tăng tốc, database thường là nơi giữ sự thật của dữ liệu.`
- `Index là trade-off để đọc nhanh hơn, đổi lấy thêm chi phí lưu trữ và update.`
- `Khi thấy chậm, câu hỏi đầu tiên là chậm ở lớp nào, không phải chậm ở công nghệ nào.`

## 6. Đề xuất tên buổi sharing

Tên khuyến nghị:

`Một request chậm đi qua hệ thống như thế nào: từ FE/mobile đến Redis và database`

Tên ngắn hơn nếu cần:

- `Từ request chậm đến Redis và database`
- `Hiểu cache và database qua hành trình của một request`

## 7. Cấu trúc 1 tiếng

### 0-5 phút: Mở bài bằng một tình huống quen thuộc

Mở bằng câu hỏi:

`App chậm thì do FE, network, API, Redis hay database?`

Mục tiêu:

- Kéo cả FE/mobile/BE vào cùng một vấn đề
- Chuyển từ mindset “công nghệ nào đúng” sang mindset “hành trình request đi qua đâu”

Speaker note:

- Không mở bằng định nghĩa Redis.
- Không mở bằng các loại index.
- Mở bằng cảm giác ai cũng từng gặp: chậm nhưng chưa biết chậm ở đâu.

### 5-15 phút: Bức tranh toàn cảnh của một request

Hình khuyên dùng:

- [146 - Chúng ta cache data ở đâu?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/146-where-do-we-cache-data.md)
- Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/146/figure-01.png)

Ý chính:

- Cache có ở browser/client, CDN, gateway, service memory, Redis, search engine và cả bên trong database.
- Redis chỉ là một lớp trong bức tranh lớn hơn.
- Mixed team sẽ bắt đầu thấy mình có liên quan tới bài này.

Speaker note:

- Dành 2-3 phút để chỉ vào từng lớp và nói lớp đó có thể giúp nhanh hơn bằng cách nào.
- Chưa cần đi sâu invalidation hay consistency ở đây.

### 15-25 phút: Mental model RAM vs ổ cứng

Hình khuyên dùng:

- [080 - Bộ nhớ máy tính hoạt động như thế nào?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/080-how-computer-memory-works.md)
- Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/080/figure-01.png)

Ý chính:

- Càng gần CPU càng nhanh nhưng càng nhỏ và đắt.
- RAM nhanh hơn disk rất nhiều nhưng không bền như disk.
- Hệ thống nhiều tầng bộ nhớ vì không có một loại storage nào vừa nhanh, vừa lớn, vừa rẻ, vừa durable.

Speaker note:

- Đây là đoạn nền tảng để giải thích Redis và database mà không cần sa vào jargon.
- Câu nói gợi nhớ: `RAM giống bàn làm việc, ổ cứng giống kho lưu trữ.`

### 25-35 phút: Redis đứng ở đâu trong hệ thống

Hình khuyên dùng:

- [154 - Vòng đời của một Redis query](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/154-the-life-of-a-redis-query.md)
- Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/154/figure-01.png)

Ý chính:

- Redis nhanh vì dữ liệu nằm trong memory.
- Redis có thể có persistence, nhưng đó không biến nó thành lựa chọn mặc định cho source of truth.
- Redis thường phù hợp cho cache, session, counter, rate limit, leaderboard, hot key lookup.

Speaker note:

- Chỉ cần nhắc AOF/RDB ở mức “Redis cũng có cách giảm mất dữ liệu”.
- Không đào quá sâu vào chi tiết fork, copy-on-write nếu room không hỏi tiếp.

### 35-45 phút: Database đọc dữ liệu thế nào, index giúp gì

Hình khuyên dùng:

- [095 - SQL query được execute trong database như thế nào?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/095-how-sql-query-executes-in-a-database.md)
- Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/095/figure-01.png)
- [106 - Các loại database index mọi developer nên biết](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/106-database-index-types-every-developer-should-know.md)
- Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/106/figure-01.png)

Ý chính:

- SQL không chạy trực tiếp từ text; database phải parse, optimize, lập execution plan rồi mới đọc/ghi.
- Index là cấu trúc phụ giúp giảm lượng dữ liệu cần scan.
- Index thường được lưu bền vững trong storage của database; phần hot của index hoặc data page được buffer trong RAM để đọc nhanh hơn.

Speaker note:

- Đây là lúc trả lời câu mà mọi người rất hay hỏi: `index nằm ở RAM hay ổ cứng?`
- Câu trả lời khuyên dùng: `Index là cấu trúc lưu trong database storage, nhưng DB cố giữ những page hay dùng trong buffer pool ở RAM để đỡ chạm disk liên tục.`

### 45-53 phút: FE/mobile/BE nên rút ra gì khi app chậm

Ý chính:

- FE/mobile:
  - giảm request thừa
  - tối ưu cache policy
  - để ý payload và network waterfall
- Backend:
  - theo dõi cache hit ratio
  - đọc execution plan
  - hiểu query pattern trước khi thêm index
- Cả team:
  - cùng dùng một mental model khi debug độ trễ

Speaker note:

- Đây là đoạn giúp audience mixed không cảm thấy buổi này chỉ dành cho backend.

### 53-60 phút: Q&A có chuẩn bị trước

Kết bằng các câu hỏi dễ bị hỏi và câu trả lời ngắn, rõ, nhất quán.

## 8. Hình ảnh nên dùng

Nên dùng `4 hình chính + 1-2 hình optional`.

Hình chính:

1. `Where Do We Cache Data`
   - File doc: [146 - Chúng ta cache data ở đâu?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/146-where-do-we-cache-data.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/146/figure-01.png)

2. `How Computer Memory Works`
   - File doc: [080 - Bộ nhớ máy tính hoạt động như thế nào?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/080-how-computer-memory-works.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/080/figure-01.png)

3. `The Life of a Redis Query`
   - File doc: [154 - Vòng đời của một Redis query](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/154-the-life-of-a-redis-query.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/154/figure-01.png)

4. `How SQL Query Executes In A Database`
   - File doc: [095 - SQL query được execute trong database như thế nào?](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/095-how-sql-query-executes-in-a-database.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/095/figure-01.png)

Hình optional:

5. `Database Index Types Every Developer Should Know`
   - File doc: [106 - Các loại database index mọi developer nên biết](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/106-database-index-types-every-developer-should-know.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/106/figure-01.png)

6. `Database Performance Cheatsheet`
   - File doc: [020 - Cheatsheet về hiệu năng database](/Users/aiot/Documents/study-english/output/bytebytego-2025/vi/020-a-cheatsheet-on-database-performance.md)
   - Asset: [figure-01.png](/Users/aiot/Documents/study-english/output/bytebytego-2025/assets/020/figure-01.png)

## 9. Cách giải thích trọng tâm

### Redis vs database

Cách nói khuyên dùng:

- `Redis giống quầy đồ đang bày sẵn trước mặt.`
- `Database giống kho chính thức của cửa hàng.`
- `Redis thường đứng trước database để giảm số lần phải chạm xuống tầng chậm hơn.`
- `Nhanh hơn không có nghĩa là thay thế hoàn toàn.`

### RAM vs ổ cứng

Cách nói khuyên dùng:

- `RAM là bàn làm việc, ổ cứng là kho.`
- `Đồ cần dùng ngay thì để trên bàn.`
- `Đồ cần giữ lâu thì để trong kho.`
- `Hệ thống thật luôn phải cân bằng giữa tốc độ và độ bền dữ liệu.`

### Index

Cách nói khuyên dùng:

- `Index giống mục lục hoặc sơ đồ kệ hàng.`
- `Không có index thì dễ phải đi tìm từng món một.`
- `Có index thì tìm nhanh hơn, nhưng phải tốn công duy trì mục lục đó mỗi khi dữ liệu đổi.`

## 10. Q&A riêng cho bố Toàn

### Nếu Redis nhanh vậy, sao không bỏ luôn database?

Trả lời ngắn:

`Vì Redis và database tối ưu cho hai bài toán khác nhau. Redis ưu tiên truy cập cực nhanh trên memory. Database ưu tiên lưu trữ bền vững, truy vấn linh hoạt, transaction và source of truth.`

### Redis có mất dữ liệu không?

Trả lời ngắn:

`Có thể. Redis vốn mạnh ở in-memory access. Nó có AOF/RDB để giảm rủi ro mất dữ liệu, nhưng chọn mức durability nào vẫn là trade-off giữa tốc độ và an toàn dữ liệu.`

### Index nằm ở RAM hay ổ cứng?

Trả lời ngắn:

`Index là cấu trúc được lưu trong storage của database, tức là gắn với disk để tồn tại lâu dài. Nhưng database sẽ cố giữ các page hay dùng của index và data trong buffer pool ở RAM để truy cập nhanh hơn.`

### Thêm index có luôn tốt không?

Trả lời ngắn:

`Không. Index thường giúp read nhanh hơn nhưng làm write chậm hơn, tốn thêm storage và chưa chắc optimizer đã dùng nếu query pattern không phù hợp.`

### FE/mobile cần quan tâm gì trong câu chuyện này?

Trả lời ngắn:

`Rất nhiều. Request quá nhiều, payload lớn, cache policy chưa hợp lý, retry chưa đúng và cách hiển thị dữ liệu đều ảnh hưởng trực tiếp tới trải nghiệm chậm. Buổi này không chỉ dành cho backend.`

### Cache có phải lúc nào cũng tốt không?

Trả lời ngắn:

`Không. Cache làm hệ thống nhanh hơn nhưng thêm vấn đề về stale data, invalidation, consistency và xóa dữ liệu ở nhiều tầng.`

## 11. Rủi ro nội dung và cách tránh

Rủi ro:

- Sa quá sâu vào Redis internals
- Sa quá sâu vào index type và execution plan
- Làm FE/mobile mất kết nối với mạch nội dung
- Nói Redis như thể là “database tốt hơn”

Cách tránh:

- Luôn quay lại câu hỏi `request đang chậm ở lớp nào`
- Mỗi đoạn kỹ thuật chỉ giữ 1 thông điệp chính
- Sau mỗi đoạn backend-ish, phải kéo lại về tác động tới sản phẩm hoặc trải nghiệm người dùng

## 12. Tiêu chí thành công

Buổi sharing được coi là thành công nếu:

1. Người nghe nhớ được ít nhất một mental model rõ ràng như `RAM vs ổ cứng` hoặc `Redis là lớp tăng tốc, database là source of truth`.
2. FE/mobile không thấy đây là buổi chỉ dành cho backend.
3. Khi kết thúc, mọi người nhìn vấn đề `app chậm` theo hướng nhiều lớp thay vì đổ ngay cho database.
4. Phần Q&A không buộc người nói phải đi quá sâu vào internals để tự bảo vệ luận điểm.

## 13. Bước tiếp theo được khuyến nghị

Sau design doc này, artifact nên làm tiếp là:

- một `sharing doc` hoàn chỉnh có speaker notes theo từng phần
- có thể xuất tiếp thành `PDF handout` hoặc slide outline sau

Trong artifact kế tiếp, nên bổ sung:

- opening script 1-2 phút
- wording ngắn cho từng hình
- closing summary 30-60 giây
- appendix Q&A mở rộng nếu muốn phòng câu hỏi khó
