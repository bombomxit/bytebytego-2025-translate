# Gợi ý trả lời riêng cho bố Toàn

## 1. Khi một màn hình trong app tải chậm, phản xạ đầu tiên của bạn thường là nghi ngờ lớp nào: client, network, API, cache hay database?

Không nên chốt ngay một lớp. Câu nên hỏi là: request này đi qua những lớp nào, và độ trễ thực sự đang nằm ở đâu.

Điểm cần chốt:

- `app chậm` không đồng nghĩa với `database chậm`
- cần tách client, network, backend, cache và database

## 2. Theo bạn, câu `app chậm` thường đang mô tả điều gì: thời gian render trên client, thời gian chờ network, thời gian xử lý backend hay thời gian đọc dữ liệu?

Nó có thể rơi vào bất kỳ lớp nào trong số đó. Vì vậy mới cần cùng một mental model về hành trình của request, thay vì đoán theo cảm giác.

Điểm cần chốt:

- người dùng chỉ cảm nhận `chậm`
- kỹ thuật cần bóc tách chậm ở lớp nào

## 3. Theo bạn, dữ liệu có thể được cache ở những đâu ngoài Redis?

Dữ liệu có thể được cache ở browser, CDN, API gateway, service memory, search engine và cả bên trong database.

Điểm cần chốt:

- Redis chỉ là một lớp cache quen thuộc
- cache thực ra xuất hiện ở rất nhiều nơi

## 4. Nếu cùng một dữ liệu xuất hiện ở browser cache, CDN, Redis và database, điều gì sẽ là khó nhất khi dữ liệu thay đổi?

Khó nhất thường là invalidation và giữ cho dữ liệu giữa các lớp đủ nhất quán với nhau.

Điểm cần chốt:

- cache giúp nhanh hơn
- nhưng thêm bài toán stale data, invalidation, consistency

## 5. Vì sao dữ liệu nằm trong RAM thường nhanh hơn dữ liệu phải đọc từ ổ cứng?

Vì RAM là tầng truy cập nhanh hơn disk rất nhiều. Có thể hình dung RAM như bàn làm việc, còn disk như kho lưu trữ.

Điểm cần chốt:

- gần CPU hơn thì nhanh hơn
- nhanh hơn thường đi kèm nhỏ hơn, đắt hơn và kém bền dữ liệu hơn

## 6. Nếu Redis nhanh như vậy, vì sao đa số hệ thống vẫn không dùng Redis để thay toàn bộ database chính?

Vì Redis và database thường tối ưu cho hai bài toán khác nhau. Redis ưu tiên tốc độ truy cập trên memory. Database chính ưu tiên durability, consistency, transaction và query capability.

Điểm cần chốt:

- Redis thường là lớp tăng tốc
- database thường là source of truth

## 7. Theo bạn, use case nào hợp với Redis hơn

Những ví dụ hợp hơn với Redis là session, rate limiting và bảng xếp hạng. Còn transaction lịch sử đơn hàng nhiều năm thường nên nằm ở database chính.

Điểm cần chốt:

- Redis hợp với dữ liệu nóng, truy cập nhanh, cấu trúc đơn giản
- dữ liệu business dài hạn thường nằm ở database

## 8. Nếu Redis là in-memory data store, vậy khi process chết hoặc máy restart thì chuyện gì có thể xảy ra?

Nếu không có persistence phù hợp thì dữ liệu có thể bị mất, hoặc khôi phục lại không đầy đủ.

Điểm cần chốt:

- đây là lý do AOF và RDB tồn tại

## 9. Theo bạn, `AOF` và `RDB` giải quyết vấn đề gì của Redis?

Chúng xử lý bài toán persistence và recovery, tức là cho Redis cách ghi dữ liệu xuống disk và dựng lại dữ liệu sau sự cố.

Điểm cần chốt:

- Redis nhanh vì memory
- AOF và RDB giúp giảm rủi ro mất dữ liệu

## 10. Nếu phải nói rất ngắn, bạn sẽ mô tả `AOF` và `RDB` khác nhau như thế nào?

AOF giống nhật ký lệnh, còn RDB giống ảnh chụp nhanh dữ liệu tại một thời điểm.

Điểm cần chốt:

- AOF: log các lệnh
- RDB: snapshot dataset

## 11. Vì sao cùng là một câu SQL nhưng lúc thì chạy nhanh, lúc thì chạy chậm?

Vì database không chỉ đọc câu SQL rồi chạy luôn. Nó còn parse, optimize và chọn execution plan. Tốc độ thực tế phụ thuộc vào execution plan, statistics, index và chuyện dữ liệu có nằm sẵn trong memory hay không.

Điểm cần chốt:

- query performance không thể nhìn bằng mắt thường từ câu SQL
- cần hiểu cách database thực thi

## 12. Theo bạn, index đang giải quyết bài toán gì trong database?

Index giúp database tìm dữ liệu nhanh hơn mà không phải quét quá nhiều row, thậm chí tránh được chuyện quét cả bảng.

Điểm cần chốt:

- index giống mục lục hoặc sơ đồ kệ hàng

## 13. Nếu thêm index thì cái giá phải trả thường là gì?

Tốn thêm storage, và các thao tác insert, update, delete đều phải tốn thêm công để duy trì index.

Điểm cần chốt:

- index tăng tốc read
- nhưng không miễn phí

## 14. Theo bạn, index nằm ở RAM hay ở ổ cứng?

Index được lưu bền vững trong storage của database, tức là gắn với disk. Nhưng những page hay dùng của index và data có thể được kéo vào RAM hoặc buffer pool để đọc nhanh hơn.

Điểm cần chốt:

- nơi lưu lâu dài là disk
- nơi tăng tốc truy cập là memory

## 15. Sau buổi này, nếu gặp một API hoặc màn hình chậm, bạn sẽ hỏi câu gì đầu tiên?

Độ trễ đang nằm ở lớp nào.

Điểm cần chốt:

- đây là câu chốt của cả buổi
- đừng hỏi ngay `database có chậm không`

## 16. Với vai trò hiện tại của bạn, bạn thấy mình có thể tác động vào lớp nào nhiều nhất để cải thiện performance?

Câu này không có một đáp án duy nhất. FE/mobile có thể tác động mạnh vào request count, payload, cache policy và rendering. Backend có thể tác động mạnh vào API shape, cache hit ratio, query pattern và index.

Điểm cần chốt:

- performance là bài toán liên lớp
- ai cũng có phần việc của mình

## Các câu chốt ngắn bố Toàn có thể nói nguyên văn

- `Cache không chỉ là Redis.`
- `Redis nhanh vì ở memory, không phải vì nó là phiên bản tốt hơn của database.`
- `Database giữ sự thật của dữ liệu, Redis thường giúp giảm số lần phải chạm vào nơi giữ sự thật đó.`
- `Index không miễn phí, nó đổi thêm chi phí duy trì để lấy tốc độ đọc.`
- `Khi app chậm, đừng hỏi ngay database có vấn đề không. Hãy hỏi độ trễ đang nằm ở lớp nào.`
