# 075 - Cách deploy service

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 160-161
- Ảnh minh họa: `../assets/075/figure-01.png`

## Hình minh họa

![How to Deploy Services](../assets/075/figure-01.png)

## Dịch sát

Deploy hoặc upgrade service là việc có rủi ro. Trong bài này, chúng ta khám phá các chiến lược giảm thiểu rủi ro.

Sơ đồ bên dưới minh họa những chiến lược phổ biến.

Multi-Service Deployment

Trong model này, chúng ta deploy thay đổi mới tới nhiều service cùng lúc. Cách tiếp cận này dễ triển khai. Nhưng vì tất cả service được upgrade cùng thời điểm, dependency rất khó quản lý và test. Rollback an toàn cũng khó.

Blue-Green Deployment

Với blue-green deployment, chúng ta có hai environment giống hệt nhau: một là staging (blue), một là production (green). Staging environment đi trước production một version. Sau khi test xong ở staging environment, user traffic được chuyển sang staging environment, và staging trở thành production. Deployment strategy này rollback đơn giản, nhưng duy trì hai environment đạt chất lượng production có thể tốn kém.

Canary Deployment

Canary deployment upgrade service dần dần, mỗi lần cho một subset user. Nó rẻ hơn blue-green deployment và dễ rollback. Tuy nhiên, vì không có staging environment, chúng ta phải test trên production. Process này phức tạp hơn vì cần monitor canary trong khi dần dần migrate ngày càng nhiều user rời khỏi old version.

A/B Test

Trong A/B test, các version khác nhau của service chạy đồng thời trên production. Mỗi version chạy một “experiment” cho một subset user. A/B test là phương pháp rẻ để test feature mới trên production. Chúng ta cần kiểm soát deployment process để tránh trường hợp một số feature bị đẩy tới user ngoài ý muốn.

Câu hỏi dành cho bạn: Bạn đã dùng deployment strategy nào? Bạn từng chứng kiến outage production liên quan đến deployment chưa, và vì sao nó xảy ra?

## Dịch nội dung trong hình

- `Multi-Service Deployment`: nhiều service A/B/C/D được nâng version đồng thời từ v1.0/v2.0/v3.0 lên v1.1/v2.1/v3.1.
- `Blue-Green Deployment`: có hai environment staging và production; upgrade/test ở staging rồi switch traffic để staging thành production.
- `Canary Deployment`: nâng một phần instance/user trước, verify rồi mới mở rộng sang toàn bộ.
- `A/B Test`: nhiều version chạy song song, ví dụ V1.1 nhận 50% traffic và V1.2 nhận 25% traffic.

## Tóm tắt & giải thích dễ hiểu

Không có deployment strategy nào tốt nhất cho mọi hệ thống. Multi-service deploy đơn giản nhưng rủi ro cao khi dependency phức tạp. Blue-green rollback nhanh nhưng tốn chi phí hạ tầng. Canary giảm blast radius nhưng đòi hỏi observability tốt. A/B test phù hợp để đo hành vi người dùng, không chỉ để giảm rủi ro kỹ thuật.

Điểm mấu chốt trong production là kiểm soát phạm vi ảnh hưởng. Nếu release lỗi, hệ thống phải phát hiện nhanh, dừng rollout và rollback hoặc disable feature trước khi ảnh hưởng quá nhiều user.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Với API thanh toán, nên dùng canary rất nhỏ, ví dụ 1% traffic nội bộ hoặc một region ít rủi ro, theo dõi error rate, latency, payment success rate và log bất thường. Với frontend feature mới, A/B test có thể đo conversion, nhưng vẫn nên dùng feature flag để tắt nhanh nếu có lỗi.

## Thuật ngữ chính

- `Deployment`: đưa version mới ra môi trường chạy thật.
- `Rollback`: quay về version cũ.
- `Blue-green deployment`: hai environment tương đương, switch traffic khi sẵn sàng.
- `Canary deployment`: rollout từng phần nhỏ.
- `A/B test`: thử nghiệm nhiều version với các nhóm user.
- `Blast radius`: phạm vi ảnh hưởng khi có lỗi.
- `Feature flag`: cờ bật/tắt feature mà không cần deploy lại.

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Câu hỏi trong tài liệu gốc.

**Câu hỏi:** Bạn đã dùng deployment strategy nào?

**Trả lời:** Với `Cách deploy service`, cách liên hệ tốt nhất là chọn một workload nhỏ rồi kiểm chứng bằng số liệu thay vì chọn theo cảm tính. Nên kiểm bằng workload nhỏ trước: latency, độ ổn định, khả năng debug, cost và rủi ro vận hành. Phần cốt lõi cần đem theo từ bài là: Không có deployment strategy nào tốt nhất cho mọi hệ thống. Multi-service deploy đơn giản nhưng rủi ro cao khi dependency phức tạp. Blue-green rollback nhanh nhưng tốn chi phí hạ tầng. Canary giảm blast radius nhưng đòi hỏi observability tốt. A/B test phù hợp để đo hành vi người dùng, không chỉ để giảm rủi ro kỹ thuật.

**Thinking học tập + liên hệ:** Khi tự liên hệ `Cách deploy service`, hãy viết ra một project cụ thể, lý do chọn công nghệ và lỗi vận hành có thể xảy ra. Lens chính là độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng. Khi đưa lên production, hãy map từng thành phần vào deploy, rollback, monitoring, alerting, secret, cost và ownership rõ ràng. Khi ghi chú lại, hãy giải thích được các keyword: `Deployment`, `Rollback`, `Blue-green deployment`, `Canary deployment`, `A/B test`.

### Câu hỏi 2

**Nguồn câu hỏi:** Câu hỏi trong tài liệu gốc.

**Câu hỏi:** Bạn từng chứng kiến outage production liên quan đến deployment chưa, và vì sao nó xảy ra?

**Trả lời:** Nếu rút thành checklist thiết kế thì ý chính là: Không có deployment strategy nào tốt nhất cho mọi hệ thống. Multi-service deploy đơn giản nhưng rủi ro cao khi dependency phức tạp. Blue-green rollback nhanh nhưng tốn chi phí hạ tầng. Canary giảm blast radius nhưng đòi hỏi observability tốt. A/B test phù hợp để đo hành vi người dùng, không chỉ để giảm rủi ro kỹ thuật. Khi áp dụng vào hệ thống thật, hãy kiểm thêm độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng.

**Thinking học tập + liên hệ:** Ôn tập `Cách deploy service` bằng cách biến khái niệm thành quyết định thiết kế cụ thể: chọn gì, bỏ gì, đo gì và ai chịu trách nhiệm. Lens chính là độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng. Khi đưa lên production, hãy map từng thành phần vào deploy, rollback, monitoring, alerting, secret, cost và ownership rõ ràng. Khi ghi chú lại, hãy giải thích được các keyword: `Deployment`, `Rollback`, `Blue-green deployment`, `Canary deployment`, `A/B test`.
