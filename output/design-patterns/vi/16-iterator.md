# 16. Iterator

[Mục lục](../README.md) · [English](../original/16-iterator.md)

## Bài toán

Cổng tài liệu liệt kê các tệp nằm trong thư mục lồng nhau để xuất dữ liệu và lập báo cáo. Hiện tại cả hai bên gọi đều có thể tự duyệt cây. Nếu sau này thư mục đổi cách biểu diễn nội bộ, mọi bên gọi đang lần theo `entries` phải sửa theo. Một số bên gọi chỉ cần tệp đầu tiên thỏa điều kiện và muốn dừng duyệt sớm.

## Mẫu thiết kế và ranh giới

Collection quyết định cách duyệt mà nó cung cấp, còn mỗi iterator giữ vị trí riêng. Bên gọi đọc các giá trị qua một giao diện duyệt chung. Nó có thể đọc tiếp, dừng hoặc bắt đầu một lượt khác mà không cần biết collection lưu phần tử thế nào.

Ví dụ dùng giao thức lặp của JavaScript. `DocumentTree` là iterable và generator do nó trả về là iterator. Collection này trả tên tệp theo thứ tự duyệt sâu, giữ nguyên thứ tự giữa các phần tử cùng cấp. Mỗi iterator giữ một ngăn xếp các phần tử chờ duyệt riêng. Đưa các phần tử cùng cấp vào ngăn xếp theo thứ tự ngược giúp lấy chúng ra đúng thứ tự ban đầu. Ví dụ giả định cây hữu hạn và giữ ổn định trong lúc duyệt.

## Ví dụ TypeScript

```typescript
type DocumentEntry =
  | Readonly<{ kind: "file"; name: string }>
  | Readonly<{ kind: "folder"; entries: readonly DocumentEntry[] }>;

class DocumentTree implements Iterable<string> {
  constructor(private readonly root: DocumentEntry) {}

  *[Symbol.iterator](): IterableIterator<string> {
    // Each traversal owns its own stack.
    const pending: DocumentEntry[] = [this.root];
    while (true) {
      const entry = pending.pop();
      if (!entry) return;
      if (entry.kind === "file") {
        yield entry.name;
      } else {
        for (let index = entry.entries.length - 1; index >= 0; index--) {
          pending.push(entry.entries[index]);
        }
      }
    }
  }
}

const tree = new DocumentTree({
  kind: "folder",
  entries: [
    { kind: "file", name: "agenda.md" },
    { kind: "folder", entries: [{ kind: "file", name: "notes.md" }] },
  ],
});
const first = tree[Symbol.iterator]();
const second = tree[Symbol.iterator]();

if (first.next().value !== "agenda.md" || first.next().value !== "notes.md") {
  throw new Error("Traversal must yield files in depth-first order");
}
if (second.next().value !== "agenda.md" || !first.next().done) {
  throw new Error("Iterators must have independent positions and signal exhaustion");
}
if ([...new DocumentTree({ kind: "folder", entries: [] })].length !== 0) {
  throw new Error("An empty folder tree must yield no files");
}
```

## Khi nên dùng

Dùng khi bên gọi cần một giao diện duyệt dùng chung, khả năng dừng sớm hoặc nhiều lượt duyệt độc lập. Với dữ liệu phân trang từ xa, cân nhắc async iterator và quy định cách hủy yêu cầu đang chạy cũng như cách báo lỗi.

### Bài toán thường gặp

- **Duyệt cây thư mục theo nhu cầu.** Một lần duyệt có thể dừng ngay khi tìm thấy tệp cần dùng. Lần duyệt khác có thể đi hết cây để lập báo cáo. Làm rõ thứ tự giữa các thư mục và tệp, và cách ứng xử nếu cây thay đổi trong lúc duyệt.
- **Đọc dữ liệu phân trang từ API.** Bộ lặp bất đồng bộ tải trang kế tiếp khi bên gọi cần thêm bản ghi. Cần giữ con trỏ phân trang riêng cho mỗi lượt duyệt và chuyển lỗi API về bên gọi. Nếu dừng sớm, giải phóng tài nguyên hoặc hủy yêu cầu còn chạy khi cần.

## Khi cách đơn giản đã đủ

Nếu dữ liệu đã là mảng và cách duyệt mặc định đáp ứng nhu cầu, dùng iterator sẵn có qua `for...of`. Có thể trả luôn một mảng kết quả khi tập kết quả nhỏ và bên gọi cần truy cập theo chỉ số.

## Đánh đổi

Bên dùng có thể phụ thuộc vào thứ tự duyệt và hành vi khi dữ liệu thay đổi trong lúc duyệt. Ghi rõ quy tắc, chẳng hạn duyệt một snapshot bất biến hoặc từ chối sửa đổi khi có lượt duyệt đang hoạt động. Duyệt theo nhu cầu giúp tránh tạo toàn bộ kết quả ngay từ đầu, còn bản cài đặt này vẫn có thể giữ nhiều phần tử cùng cấp đang chờ trong bộ nhớ.

## Bài tập

Tạo thư mục có một thư mục con rỗng nằm giữa hai tệp. Kiểm tra chỉ có hai tệp được trả về theo đúng thứ tự ban đầu. Sau khi dừng ở tệp đầu tiên, tạo một iterator mới và kiểm tra nó bắt đầu từ đầu.

## Tài liệu tham khảo

- [Iterator · Refactoring.Guru](https://refactoring.guru/design-patterns/iterator)

[← Chương trước · 15. Interpreter](15-interpreter.md) · [Chương sau → · 17. Mediator](17-mediator.md)
