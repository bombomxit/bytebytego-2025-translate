# 23. Visitor

[Mục lục](../README.md) · [English](../original/23-visitor.md)

## Bài toán

Trình soạn thảo lưu tài liệu dưới dạng cây gồm các node mục, đoạn văn và tệp đính kèm. Nhóm cần báo cáo kích thước tệp ngay bây giờ và báo cáo liên kết hỏng ở bước tiếp theo. Khi các loại node ổn định nhưng báo cáo liên tục tăng, thêm phương thức cho từng báo cáo vào mỗi node sẽ khiến mỗi lần thay đổi báo cáo phải sửa nhiều lớp trong mô hình trình soạn thảo.

## Mẫu thiết kế và ranh giới

Mỗi phần tử cung cấp `accept(visitor)` và gọi phương thức của visitor ứng với kiểu cụ thể của nó. Triển khai của phần tử xác định phương thức theo kiểu. Visitor do bên gọi truyền vào xác định phần triển khai nào sẽ chạy. Hai bước dispatch kết hợp để chọn thao tác cho từng loại phần tử.

Ở ví dụ này, node mục tiếp nhận visitor rồi chuyển việc duyệt xuống các node con. Phép tính kích thước nằm trong một visitor riêng. Cần xác định sớm ai quản lý việc duyệt cây. Nếu thao tác sau này cần bỏ qua một cây con hoặc thay đổi thứ tự duyệt, hãy cấp cho nó API duyệt cây có khả năng điều khiển đó.

## Ví dụ TypeScript

```typescript
interface DocumentElement {
  accept(visitor: DocumentVisitor): void;
}

interface DocumentVisitor {
  visitSection(section: Section): void;
  visitParagraph(paragraph: Paragraph): void;
  visitAttachment(attachment: Attachment): void;
}

class Section implements DocumentElement {
  constructor(readonly children: readonly DocumentElement[]) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitSection(this);
    for (const child of this.children) child.accept(visitor);
  }
}

class Paragraph implements DocumentElement {
  constructor(readonly text: string) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitParagraph(this);
  }
}

class Attachment implements DocumentElement {
  constructor(readonly bytes: number) {}

  accept(visitor: DocumentVisitor): void {
    visitor.visitAttachment(this);
  }
}

class AttachmentSize implements DocumentVisitor {
  totalBytes = 0;

  visitSection(_section: Section): void {}

  visitParagraph(_paragraph: Paragraph): void {}

  visitAttachment(attachment: Attachment): void {
    this.totalBytes += attachment.bytes;
  }
}

const tree = new Section([
  new Paragraph("Release notes"),
  new Attachment(200),
  new Section([new Attachment(550)]),
]);

const report = new AttachmentSize();
tree.accept(report);
if (report.totalBytes !== 750) throw new Error("Expected 750 attachment bytes");

const paragraph = new Paragraph("No attachments");
const emptyReport = new AttachmentSize();
paragraph.accept(emptyReport);
if (emptyReport.totalBytes !== 0) throw new Error("Expected zero attachment bytes");
```

## Khi nên dùng

Dùng Visitor khi tập loại phần tử ổn định và thường có thêm thao tác xử lý mỗi loại theo cách riêng. Interface của visitor buộc mỗi thao tác khai báo rõ cách xử lý các loại phần tử được hỗ trợ.

## Khi cách đơn giản đã đủ

Discriminated union kèm switch bao phủ đầy đủ có thể dễ đọc hơn nếu chỉ có vài thao tác và các phần tử là dữ liệu thuần. Một vòng lặp nhận callback thường đủ nếu xử lý mọi phần tử theo cùng một cách.

## Đánh đổi

Thêm một thao tác chỉ cần thêm visitor. Thêm một loại phần tử làm đổi interface và có thể buộc cập nhật mọi visitor. Với visitor có trạng thái, cần nêu rõ vòng đời. Ví dụ này tạo một instance cho mỗi báo cáo.

## Bài tập

Viết visitor thứ hai để đếm đoạn văn. Cây trong ví dụ phải cho kết quả một đoạn văn và vẫn báo 750 byte tệp đính kèm. Các lớp node hiện tại phải dùng được với cả hai visitor.

## Tài liệu tham khảo

- [Visitor · Refactoring.Guru](https://refactoring.guru/design-patterns/visitor)

[← Chương trước · 22. Template Method](22-template-method.md) · [Chương sau → · Cách chọn mẫu thiết kế](24-chon-mau.md)
