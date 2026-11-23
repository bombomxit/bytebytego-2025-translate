# 02. Abstract Factory

[Mục lục](../README.md) · [English](../original/02-abstract-factory.md)

## Bài toán

Cổng nội bộ gửi gói tài liệu tới hai hệ thống lưu trữ. Mỗi hệ thống dùng định dạng gói và quy ước biên nhận riêng. Nếu đường xuất tài liệu chọn writer và bộ đọc biên nhận độc lập, một cấu hình triển khai có thể tải gói lên thành công rồi gặp lỗi khi đọc xác nhận. Khi có nhà cung cấp thứ ba, ứng dụng nên chỉ cần thêm một lựa chọn tích hợp.

## Mẫu thiết kế và ranh giới

`ArchiveFactory` khai báo phương thức tạo hai product liên quan là `EnvelopeWriter` và `ReceiptReader`. Mỗi factory cụ thể cung cấp cả hai product của cùng một hệ thống lưu trữ. `recordDocument()` nhận một factory và lấy cặp product qua factory đó. Việc chọn nhà cung cấp diễn ra ở ranh giới ứng dụng. Use case dựa vào hợp đồng của product và tính tương thích mà factory cam kết.

## Ví dụ TypeScript

Ví dụ dùng chuỗi để biểu diễn định dạng truyền dữ liệu của từng nhà cung cấp. Bên gọi truyền vào biên nhận mà hệ thống lưu trữ sẽ trả về sau khi nhận gói. Cả hai cặp cho ra cùng cấu trúc kết quả ở tầng ứng dụng. Phép kiểm tra cuối mô phỏng lỗi khi đưa biên nhận vào nhầm tích hợp.

```typescript
interface EnvelopeWriter {
  encode(documentId: string): string
}

interface ReceiptReader {
  read(receipt: string): string
}

interface ArchiveFactory {
  createWriter(): EnvelopeWriter
  createReceiptReader(): ReceiptReader
}

class ArchiveAFactory implements ArchiveFactory {
  createWriter(): EnvelopeWriter {
    return { encode: id => JSON.stringify({ record: id }) }
  }

  createReceiptReader(): ReceiptReader {
    return {
      read(receipt) {
        if (!receipt.startsWith("A-")) throw new Error("Archive A receipt expected")
        return receipt.slice(2)
      },
    }
  }
}

class ArchiveBFactory implements ArchiveFactory {
  createWriter(): EnvelopeWriter {
    return { encode: id => "document=" + encodeURIComponent(id) }
  }

  createReceiptReader(): ReceiptReader {
    return {
      read(receipt) {
        if (!receipt.startsWith("B/")) throw new Error("Archive B receipt expected")
        return receipt.slice(2)
      },
    }
  }
}

function recordDocument(factory: ArchiveFactory, documentId: string, receipt: string) {
  const body = factory.createWriter().encode(documentId)
  const reference = factory.createReceiptReader().read(receipt)
  return { body, reference }
}

const archiveA = new ArchiveAFactory()
const archiveB = new ArchiveBFactory()
const recordA = recordDocument(archiveA, "D 12", "A-401")
if (recordA.body !== '{"record":"D 12"}' || recordA.reference !== "401") {
  throw new Error("Archive A must use the matching pair")
}
const recordB = recordDocument(archiveB, "D 12", "B/811")
if (recordB.body !== "document=D%2012" || recordB.reference !== "811") {
  throw new Error("Archive B must use the matching pair")
}

let rejected = false
try {
  recordDocument(archiveB, "D 12", "A-401")
} catch (error) {
  rejected = error instanceof Error && error.message === "Archive B receipt expected"
}
if (!rejected) throw new Error("A receipt from the wrong family must be rejected")
```

## Khi nên dùng

Dùng Abstract Factory khi bên gọi cần nhiều product cùng họ và việc trộn các họ có thể vi phạm ràng buộc về phiên bản giao thức, nhà cung cấp hay chủ đề giao diện. Chọn họ một lần cho mỗi use case hoặc phạm vi cấu hình. Khi phải định tuyến theo tenant trong lúc chạy, tầng ứng dụng vẫn cần chính sách chọn họ cho tenant đó.

### Bài toán thường gặp

- **Tích hợp nhà cung cấp ký số.** Mỗi nhà cung cấp có bộ gửi yêu cầu ký, kiểm tra trạng thái và xác minh kết quả theo cùng giao thức của họ. Chọn nhà máy một lần cho một giao dịch ký để cả ba bước dùng cùng nhà cung cấp.
- **Bộ giao diện theo chủ đề.** Mỗi chủ đề tạo nút, hộp thoại và trường nhập liệu theo cùng quy chuẩn hiển thị. Mẫu này có ích khi các thành phần thực sự có triển khai riêng theo chủ đề. Dùng biến giao diện hoặc bảng màu nếu khác biệt chỉ nằm ở màu và kích thước.

## Khi cách đơn giản đã đủ

Nếu tích hợp chỉ cung cấp một đối tượng nhỏ, hãy truyền trực tiếp đối tượng đó. Nếu các thành phần đã được tạo cùng nhau lúc khởi động, hãy truyền một đối tượng có kiểu rõ ràng chứa các thành phần cộng tác. Cách này giữ các thành phần cùng nhà cung cấp đi với nhau với ít mã khởi tạo hơn. Factory Method cung cấp một phương thức tạo đối tượng có thể ghi đè. Abstract Factory gom việc tạo nhiều product liên quan.

## Đánh đổi

- Thêm nhà cung cấp nghĩa là bổ sung một bản triển khai của factory và các product tương ứng. Thêm vai trò product mới làm thay đổi interface của factory và mọi họ.
- Interface quy định cấu trúc của product. Cần contract test để kiểm tra tính tương thích vì các product có cùng interface TypeScript vẫn có thể đòi hỏi định dạng truyền khác nhau.
- Xác định vòng đời của adapter thực tế. Factory có thể tạo adapter cho mỗi thao tác hoặc trả về các đối tượng có vòng đời do ứng dụng quản lý.

## Bài tập

Thêm hệ thống lưu trữ thứ ba có biên nhận bắt đầu bằng `C-`. Biên nhận đúng họ phải được chấp nhận, biên nhận `A-` phải bị từ chối và `recordDocument()` phải chạy mà không cần thêm nhánh theo nhà cung cấp.

## Tài liệu tham khảo

- [Refactoring.Guru · Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory)

[← Chương trước · 01. Factory Method](01-factory-method.md) · [Chương sau → · 03. Builder](03-builder.md)
