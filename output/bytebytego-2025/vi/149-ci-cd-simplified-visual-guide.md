# 149 - Visual guide đơn giản về CI/CD

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 308-309
- Ảnh minh họa: `../assets/149/figure-01.png`

## Hình minh họa

![CI/CD Simplified Visual Guide](../assets/149/figure-01.png)

## Dịch sát

Dù bạn là developer, DevOps specialist, tester, hoặc tham gia bất kỳ modern IT role nào, CI/CD pipeline đã trở thành một phần integral của software development process.

Continuous Integration (CI) là practice trong đó code change được combine thường xuyên vào shared repository. Process này gồm automatic check để bảo đảm code mới hoạt động tốt với existing code.

Continuous Deployment (CD) chịu trách nhiệm tự động đưa các code change này vào real-world use. Nó bảo đảm process chuyển code mới lên production mượt và reliable.

Visual guide này được thiết kế để giúp bạn nắm bắt và cải thiện method tạo và deliver software hiệu quả hơn.

## Dịch nội dung trong hình

- Developer làm việc trên `feature branch`, code ready thì gửi PR.
- CI chạy application build from source code, checking code quality và running unit tests.
- Nếu fail, developer sửa bug và gửi lại.
- Nếu pass, PR được review/approve rồi merge vào main.
- CD pipeline build image, chạy code analysis, unit/integration/security scanning.
- Image ready thì deploy tới K8S cluster và deployment successful.

## Tóm tắt & giải thích dễ hiểu

CI giúp phát hiện lỗi sớm trước khi code vào main. CD giúp biến artifact đã kiểm tra thành deployment lặp lại được. Pipeline tốt giảm thao tác thủ công, giảm lỗi release và tăng tốc feedback loop.

## Ví dụ thực tế - không nằm trong tài liệu gốc

Một pull request có thể chạy lint, unit test, typecheck và build Docker image. Sau khi merge main, pipeline push image lên registry, cập nhật Helm chart, ArgoCD sync staging, chạy smoke test rồi promote production bằng manual approval hoặc canary.

## Thuật ngữ chính

- `CI`: Continuous Integration.
- `CD`: Continuous Deployment/Delivery.
- `Feature branch`: branch làm feature.
- `Pull request`: yêu cầu review/merge code.
- `Static analysis`: phân tích code không cần chạy.
- `Security scanning`: quét lỗ hổng.
- `K8S`: Kubernetes.

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Suy ra từ tiêu đề/nội dung chính vì bài gốc không có câu hỏi riêng.

**Câu hỏi:** Sau khi đọc bài “CI/CD Simplified Visual Guide”, ý chính cần trả lời và áp dụng vào system design là gì?

**Trả lời:** Trọng tâm cần đem vào thực tế là: CI giúp phát hiện lỗi sớm trước khi code vào main. CD giúp biến artifact đã kiểm tra thành deployment lặp lại được. Pipeline tốt giảm thao tác thủ công, giảm lỗi release và tăng tốc feedback loop. Khi áp dụng vào hệ thống thật, hãy kiểm thêm độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng.

**Thinking học tập + liên hệ:** Ôn tập `Visual guide đơn giản về CI/CD` bằng cách biến khái niệm thành quyết định thiết kế cụ thể: chọn gì, bỏ gì, đo gì và ai chịu trách nhiệm. Lens chính là độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng. Khi đưa lên production, hãy map từng thành phần vào deploy, rollback, monitoring, alerting, secret, cost và ownership rõ ràng. Khi ghi chú lại, hãy giải thích được các keyword: `CI`, `CD`, `Feature branch`, `Pull request`, `Static analysis`.
