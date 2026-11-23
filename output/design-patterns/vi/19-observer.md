# 19. Observer

[Mục lục](../README.md) · [English](../original/19-observer.md)

## Bài toán

Khi một tài liệu được công bố, một thành phần cập nhật chỉ mục cục bộ và thành phần khác ghi lại số phiên bản vào nhật ký cục bộ. Giao diện sau này có thể đăng ký để làm mới danh sách. Nếu bên phát sự kiện phải biết từng bên nhận, mỗi phản ứng mới đều buộc sửa luồng công bố.

## Mẫu thiết kế và ranh giới

Cung cấp giao diện đăng ký cho một sự kiện có kiểu rõ ràng. Subject quản lý các đăng ký và thông báo cho observer đang hoạt động khi sự kiện xảy ra. Mỗi observer chịu trách nhiệm về cách phản ứng. Bên phát chỉ cần biết cấu trúc sự kiện và giao diện đăng ký.

`DocumentPublisher` là subject. Các callback chỉ mục và nhật ký là observer. Mỗi lần gọi `subscribe` trả về một hàm hủy đăng ký tương ứng. Bản cài đặt này chụp danh sách đăng ký vào đầu lượt thông báo. Các thay đổi đăng ký tác động đến sự kiện về sau, kể cả sự kiện mà một callback phát lồng trong lượt đang chạy. Thông báo được gửi đồng bộ theo thứ tự đăng ký. Callback ném ngoại lệ sẽ ngắt việc thông báo cho các observer phía sau.

## Ví dụ TypeScript

```typescript
type DocumentPublished = Readonly<{ documentId: string; revision: number }>;
type PublishedObserver = (event: DocumentPublished) => void;

class DocumentPublisher {
  private readonly observers = new Set<PublishedObserver>();

  subscribe(observer: PublishedObserver): () => void {
    // A wrapper gives each subscription its own identity.
    const subscription = (event: DocumentPublished) => observer(event);
    this.observers.add(subscription);
    return () => { this.observers.delete(subscription); };
  }

  publish(documentId: string, revision: number): void {
    const event = Object.freeze({ documentId, revision });
    for (const observer of [...this.observers]) {
      observer(event);
    }
  }
}

const publisher = new DocumentPublisher();
const indexed: string[] = [];
const journal: number[] = [];

const stopIndexing = publisher.subscribe(event => indexed.push(event.documentId));
publisher.subscribe(event => journal.push(event.revision));

publisher.publish("proposal", 1);
if (indexed.join() !== "proposal" || journal.join() !== "1") {
  throw new Error("Each active observer must receive the first event");
}

stopIndexing();
publisher.publish("minutes", 2);
if (indexed.join() !== "proposal" || journal.join() !== "1,2") {
  throw new Error("Unsubscribing one observer must leave the others active");
}
```

## Khi nên dùng

Dùng Observer khi nhiều bên nhận độc lập trong cùng tiến trình cần cùng sự kiện và danh sách hoặc vòng đời của chúng có thể đổi. Gắn việc hủy đăng ký với vòng đời của đối tượng như thành phần giao diện.

### Bài toán thường gặp

- **Phản ứng khi tài liệu được công bố.** Bên phát đưa ra sự kiện chứa mã tài liệu và phiên bản. Danh sách đang mở có thể tải lại, còn bộ đếm cập nhật số lượng. Các phản ứng độc lập có thể đăng ký riêng. Nếu cập nhật nào bắt buộc để thao tác công bố thành công, giữ nó trong luồng xử lý chính.
- **Đồng bộ giao diện với mô hình soạn thảo.** Thanh trạng thái theo dõi thay đổi số từ, còn cây mục lục theo dõi cấu trúc đề mục. Hủy đăng ký khi đóng cửa sổ. Xác định cách xử lý ngoại lệ nếu các bên khác vẫn phải nhận thông báo khi một bên theo dõi gặp lỗi.

## Khi cách đơn giản đã đủ

Một phản ứng duy nhất và ổn định có thể gọi trực tiếp. Dùng một luồng điều phối tường minh khi nhiều bước phải hoàn thành theo thứ tự cụ thể thì ca sử dụng mới được coi là thành công.

## Đánh đổi

Tác dụng phụ khó thấy hơn ở nơi phát sự kiện. Quy định thứ tự listener, việc phát sự kiện lồng nhau và ảnh hưởng của ngoại lệ tới bên phát cùng các listener khác. Ví dụ thông báo trong bộ nhớ, không lưu bền vững và không tự động retry. Giao tiếp qua nhiều tiến trình cần quy tắc giao nhận riêng, trong đó có cách xử lý bản tin trùng và thứ tự khi các yếu tố này quan trọng.

## Bài tập

Đăng ký cùng một callback hai lần rồi hủy đăng ký thứ nhất. Phát sự kiện mới và kiểm tra callback chỉ chạy một lần. Sau đó hủy cả hai lượt đăng ký và kiểm tra lần phát tiếp theo không đổi số lần callback đã chạy.

## Tài liệu tham khảo

- [Observer · Refactoring.Guru](https://refactoring.guru/design-patterns/observer)

[← Chương trước · 18. Memento](18-memento.md) · [Chương sau → · 20. State](20-state.md)
