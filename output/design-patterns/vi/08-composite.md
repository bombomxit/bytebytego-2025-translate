# 08. Composite

[Mục lục](../README.md) · [English](../original/08-composite.md)

## Bài toán

Màn hình xuất tài liệu cho phép chọn một tài liệu hoặc cả thư mục. Trước khi đóng gói, hệ thống cần kiểm tra tổng kích thước đầu vào có nằm trong giới hạn hay không. Một thư mục có thể chứa tài liệu và thư mục con. Màn hình, worker xử lý theo lô và công cụ dòng lệnh đều cần cùng cách tính. Nếu từng bên gọi tự duyệt cây, việc thêm một loại mục xuất có thể phải sửa ở nhiều nơi.

## Mẫu thiết kế và ranh giới

Composite dùng một interface nhỏ chung cho nút lá và nút chứa. Trong ví dụ, `ArchivePart` là thành phần chung. Nút lá tài liệu đóng góp kích thước của chính nó. Thư mục thực hiện cùng thao tác bằng cách hỏi kích thước từng mục con rồi cộng lại. Bên gọi `fitsLimit` làm việc với `ArchivePart` ở mọi độ sâu. Đưa các thao tác mà mọi thành phần đều hỗ trợ vào interface chung. Khi cần thêm hoặc xóa mục con, hãy đặt thao tác đó trên interface của thư mục.

## Ví dụ TypeScript

Kiểm tra một tài liệu và kiểm tra gói lồng nhau dùng chung thao tác so với giới hạn. Ví dụ giả định số byte của từng tài liệu lấy từ metadata đáng tin cậy và giới hạn đã được xác thực. Mỗi kích thước, tổng kích thước và giới hạn đều là số nguyên không âm trong miền số nguyên an toàn của JavaScript. Thư mục rỗng được tính là 0. Header của tệp nén, tỷ lệ nén và các phần phát sinh khác thuộc một phép ước tính riêng.

```typescript
interface ArchivePart {
  contentBytes(): number;
}

class ArchiveDocument implements ArchivePart {
  constructor(private readonly bytes: number) {}

  contentBytes(): number {
    return this.bytes;
  }
}

class ArchiveFolder implements ArchivePart {
  private readonly children: readonly ArchivePart[];

  constructor(...children: ArchivePart[]) {
    this.children = children;
  }

  contentBytes(): number {
    return this.children.reduce((total, child) => total + child.contentBytes(), 0);
  }
}

function fitsLimit(part: ArchivePart, limitBytes: number): boolean {
  return part.contentBytes() <= limitBytes;
}

const contract = new ArchiveDocument(140);
const empty = new ArchiveFolder();
const bundle = new ArchiveFolder(
  contract,
  new ArchiveFolder(new ArchiveDocument(60), empty),
);

if (!fitsLimit(contract, 140) || empty.contentBytes() !== 0) {
  throw new Error("A document and an empty folder should each be measurable");
}
if (bundle.contentBytes() !== 200 || fitsLimit(bundle, 199)) {
  throw new Error("A nested bundle should include every document");
}
```

## Khi nên dùng

Dùng khi dữ liệu có phân cấp thực sự và thao tác trên nhóm có thể suy ra nhất quán từ các thành phần con. Ví dụ thường gặp là cộng tổng, kết xuất các phần theo thứ tự và áp dụng một quy tắc lên cây con. Việc thêm loại nút lá có thể chỉ cần sửa cục bộ nếu nó đáp ứng hợp đồng hiện có.

## Khi cách đơn giản đã đủ

Nếu cấu trúc cây ít thay đổi và chỉ có một thao tác duyệt, một discriminated union và một hàm đệ quy có thể rõ hơn. Nếu việc phân nhóm không ảnh hưởng nghiệp vụ, danh sách phẳng và phép cộng là đủ.

## Đánh đổi

Interface chung nên tránh cam kết các thao tác mà một số loại nút không hỗ trợ được. Phép duyệt đi qua mọi mục và có thể làm tràn ngăn xếp nếu cây quá sâu. Ví dụ mô hình hóa cây các mục đóng gói và đếm tài liệu mỗi lần nó được đưa vào gói. Nếu mô hình thật có shortcut hoặc liên kết, cần quy định cách xử lý chu trình và tham chiếu lặp trước khi duyệt.

## Bài tập

Thêm nút lá đại diện cho tệp manifest được sinh ra với số byte đã biết. Đặt nó trong một thư mục lồng nhau rồi chứng minh phép kiểm tra giới hạn thay đổi mà không cần sửa `ArchiveFolder` hay `fitsLimit`.

## Tài liệu tham khảo

- [Composite — Refactoring.Guru](https://refactoring.guru/design-patterns/composite)

[← Chương trước · 07. Bridge](07-bridge.md) · [Chương sau → · 09. Decorator](09-decorator.md)
