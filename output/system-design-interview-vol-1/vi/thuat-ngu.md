# Thuật ngữ System Design

Bảng tham khảo tự biên soạn để thống nhất cách dùng từ khi học và dịch. Có thể điều chỉnh theo ngữ cảnh của tài liệu nguồn.

| Thuật ngữ | Cách dùng tiếng Việt | Ý nghĩa ngắn |
| --- | --- | --- |
| Scalability | Khả năng mở rộng | Khả năng đáp ứng tải tăng bằng cách bổ sung hoặc tăng năng lực tài nguyên. |
| Availability | Tính sẵn sàng | Mức độ hệ thống có thể phục vụ khi người dùng cần. |
| Reliability | Độ tin cậy | Khả năng hoạt động đúng trong điều kiện và khoảng thời gian xác định. |
| Latency | Độ trễ | Thời gian từ một mốc bắt đầu đến một mốc kết thúc của thao tác; cần nêu rõ hai mốc khi đo. |
| Throughput | Thông lượng | Lượng công việc xử lý được trong một đơn vị thời gian. |
| Load balancer | Bộ cân bằng tải | Thành phần phân phối yêu cầu đến các tài nguyên xử lý. |
| Cache | Bộ nhớ đệm | Nơi giữ dữ liệu có thể dùng lại để giảm chi phí truy xuất hoặc tính toán. |
| Replication | Sao chép dữ liệu | Duy trì các bản sao dữ liệu trên nhiều nút theo cơ chế đồng bộ xác định. |
| Sharding | Phân mảnh dữ liệu | Chia dữ liệu thành các phần đặt trên những nút hoặc nhóm nút khác nhau. |
| Consistency | Tính nhất quán | Các bảo đảm về dữ liệu mà thao tác đọc có thể quan sát sau những thao tác ghi. |
| Message queue | Hàng đợi thông điệp | Cơ chế lưu và chuyển thông điệp giữa bên gửi và bên xử lý. |
| Trade-off | Sự đánh đổi | Lựa chọn chấp nhận chi phí hoặc hạn chế ở một mặt để đạt lợi ích ở mặt khác. |
| Rate limiter | Bộ giới hạn tốc độ | Thành phần giới hạn số yêu cầu hoặc thao tác trong một khoảng thời gian. |
| Consistent hashing | Băm nhất quán | Cách phân bố khóa giúp hạn chế việc di chuyển dữ liệu khi tập nút thay đổi. |
| Partition tolerance | Khả năng chịu phân vùng mạng | Khả năng ứng phó khi một số nhóm nút không thể liên lạc với nhau. |
| Eventual consistency | Tính nhất quán cuối cùng | Các bản sao hội tụ về cùng trạng thái khi việc cập nhật dừng và các điều kiện đồng bộ được đáp ứng. |
| Failover | Chuyển đổi dự phòng | Chuyển công việc sang thành phần thay thế khi thành phần đang phục vụ gặp sự cố. |
| Redundancy | Tính dự phòng | Duy trì thêm tài nguyên hoặc bản sao để giảm tác động khi một thành phần hỏng. |
| Single point of failure | Điểm lỗi đơn | Thành phần mà sự cố của riêng nó có thể làm cả chức năng hoặc hệ thống ngừng hoạt động. |
| DAU | Người dùng hoạt động hằng ngày | Số người dùng khác nhau hoạt động trong một ngày theo định nghĩa của sản phẩm. |
| QPS | Số truy vấn mỗi giây | Đơn vị biểu diễn tốc độ truy vấn; cần phân biệt với số yêu cầu HTTP hoặc giao dịch. |
| Fanout | Phân phát đến nhiều đích | Từ một sự kiện hoặc dữ liệu đầu vào, tạo việc phân phối đến nhiều nơi nhận. |
| Deduplication | Khử trùng lặp | Phát hiện và tránh lưu hoặc xử lý nhiều lần cùng một nội dung. |
| Delta synchronization | Đồng bộ phần thay đổi | Chỉ trao đổi phần khác biệt thay vì truyền lại toàn bộ dữ liệu. |
