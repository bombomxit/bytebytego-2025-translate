# 162 - TCP vs UDP

- Nguồn: ByteByteGo Big Archive System Design 2025
- Trang PDF: 334
- Ảnh minh họa: `../assets/162/figure-01.png`

## Hình minh họa

![TCP vs UDP](../assets/162/figure-01.png)

## Dịch sát

Mỗi lần data di chuyển qua internet, nó chọn giữa accuracy và speed. Đó là TCP vs UDP.

TCP: Connection-oriented và reliable. Nó bảo đảm delivery có thứ tự, không duplicate, với flow control và congestion control, nên lý tưởng cho web browsing, email và file transfer.

UDP: Connectionless và lightweight. Nó gửi packet mà không guarantee delivery hoặc order, nhưng overhead tối thiểu. Nó hoàn hảo cho gaming, streaming và real-time communication.

## Dịch nội dung trong hình

- `Connection`: TCP connection-oriented qua handshake; UDP connectionless gửi request trực tiếp.
- `Service Target`: TCP thường unicast; UDP hỗ trợ unicast, multicast, broadcast.
- `Header Size`: TCP header lớn hơn, có sequence/ack/window/checksum/options; UDP header nhỏ hơn gồm source port, destination port, length, checksum.
- `Reliability`: TCP reliable delivery, duplicate removal, retransmission; UDP best-effort, no guarantee.
- `Flow Control`: TCP có flow/congestion control; UDP không có flow control/congestion control built-in.

## Tóm tắt & giải thích dễ hiểu

TCP ưu tiên đúng và đủ: dữ liệu đến theo thứ tự, mất gói thì gửi lại, có kiểm soát tốc độ. UDP ưu tiên nhanh và nhẹ: gửi gói đi ngay, app tự xử lý mất gói nếu cần. Chọn TCP hay UDP phụ thuộc yêu cầu: file/API cần đúng dữ liệu, video/game/voice cần realtime hơn.

## Ví dụ thực tế - không nằm trong tài liệu gốc

HTTP/1.1 và HTTP/2 chạy trên TCP vì web/API cần dữ liệu đúng. DNS thường dùng UDP để nhanh. Game online dùng UDP để giảm latency, vì một vài packet cũ bị mất có thể không đáng gửi lại nếu state mới đã đến.

## Thuật ngữ chính

- `TCP`: Transmission Control Protocol.
- `UDP`: User Datagram Protocol.
- `Connection-oriented`: cần thiết lập kết nối.
- `Connectionless`: không cần kết nối trước.
- `Flow control`: kiểm soát tốc độ giữa sender/receiver.
- `Congestion control`: tránh làm nghẽn mạng.
- `Retransmission`: gửi lại packet bị mất.

