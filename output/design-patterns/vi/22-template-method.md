# 22. Template Method

[Mục lục](../README.md) · [English](../original/22-template-method.md)

## Bài toán

Một lượt xuất tài liệu luôn đi qua cùng thứ tự. Dịch vụ chuẩn hóa tiêu đề, tạo nội dung theo định dạng đích rồi gắn mã tài liệu. Bản văn bản và bản JSON dùng chung quy tắc chuẩn hóa và metadata. Nếu lặp lại quy trình trong từng exporter, định dạng mới dễ bỏ sót một bước hoặc chạy sai thứ tự.

## Mẫu thiết kế và ranh giới

Lớp cơ sở nắm thứ tự xử lý trong template method. Hàm này gọi một bước trừu tượng có phạm vi protected để từng lớp con triển khai. Trong thiết kế này, `export()` định nghĩa cả quy trình, còn `render()` quyết định cách biểu diễn nội dung. Lớp cha gọi hành vi cụ thể của lớp con tại đúng điểm trong quy trình.

Trong TypeScript, lớp con vẫn có thể ghi đè phương thức public dù thiết kế coi phương thức đó là cố định. Nếu bắt buộc phải giữ nguyên thứ tự khi chạy, có thể dùng hàm ở cấp module, truyền các bước xử lý vào hàm và chỉ công khai hàm đó làm điểm vào.

## Ví dụ TypeScript

```typescript
type SourceDocument = Readonly<{ id: string; title: string }>;

abstract class DocumentExporter {
  export(document: SourceDocument): { documentId: string; body: string } {
    const title = document.title.trim().replace(/\s+/g, " ");
    const body = this.render(title);
    return { documentId: document.id, body };
  }

  protected abstract render(title: string): string;
}

class TextExporter extends DocumentExporter {
  protected render(title: string): string {
    return title;
  }
}

class JsonExporter extends DocumentExporter {
  protected render(title: string): string {
    return JSON.stringify({ title });
  }
}

const documentToExport = { id: "doc-8", title: "  Release   notes  " };
const text = new TextExporter().export(documentToExport);
const json = new JsonExporter().export(documentToExport);

if (text.documentId !== "doc-8" || text.body !== "Release notes") {
  throw new Error("Text should contain the normalized title and preserve the ID");
}
if (json.documentId !== "doc-8" || json.body !== '{"title":"Release notes"}') {
  throw new Error("JSON should receive the same normalized title");
}
```

## Khi nên dùng

Dùng Template Method khi các triển khai liên quan có chung một trình tự cần được cập nhật tại một nơi, với một vài điểm thay đổi đã xác định. Mẫu phù hợp khi mỗi lớp con thực sự là một dạng chuyên biệt của lớp cơ sở.

### Bài toán thường gặp

- **Nhập dữ liệu từ nhiều định dạng.** Lớp cơ sở luôn thực hiện đọc, kiểm tra dữ liệu và báo kết quả theo cùng trình tự. Lớp con biết cách chuyển dòng CSV hoặc bản ghi JSON sang cấu trúc chung. Thêm định dạng bằng cách triển khai bước đọc trong khi giữ các bước kiểm tra chung.
- **Xuất tài liệu theo một chuẩn chung.** Các lớp xuất giữ chung thứ tự chuẩn hóa tiêu đề, kết xuất nội dung rồi gắn mã tài liệu. Mỗi lớp con thay phần kết xuất theo định dạng của mình. Nếu chỉ khác một phép biến đổi và không cần mô hình kế thừa, truyền một hàm kết xuất vào quy trình chung.

## Khi cách đơn giản đã đủ

Một hàm xuất độc lập nhận callback định dạng thường đủ nếu chỉ khác cách định dạng. Chọn Strategy khi bên gọi cần chọn hoặc thay quy tắc định dạng trong lúc chương trình chạy.

## Đánh đổi

Dễ thay đổi thứ tự chung tại một chỗ. Lớp con phụ thuộc vào API protected và điều kiện mà lớp cha gọi từng bước. Giữ các hook nhỏ, mô tả rõ dữ liệu chúng nhận và xem việc đổi thứ tự gọi hook là thay đổi hợp đồng.

## Bài tập

Thêm exporter Markdown dùng tiêu đề đã chuẩn hóa để tạo heading. Kiểm tra kết quả giữ đúng mã tài liệu gốc và các kiểm tra của bản văn bản, JSON vẫn qua.

## Tài liệu tham khảo

- [Template Method · Refactoring.Guru](https://refactoring.guru/design-patterns/template-method)

[← Chương trước · 21. Strategy](21-strategy.md) · [Chương sau → · 23. Visitor](23-visitor.md)
