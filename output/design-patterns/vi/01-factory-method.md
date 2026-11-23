# 01. Factory Method

[Mục lục](../README.md) · [English](../original/01-factory-method.md)

## Bài toán

Cổng nội bộ hỗ trợ xuất danh sách hồ sơ từ quy trình phê duyệt. Mỗi lượt xuất đọc các dòng, chuẩn hóa tên hiển thị rồi trả về nội dung kèm kiểu nội dung (media type). Ban đầu cổng xuất văn bản thuần, sau đó cần thêm JSON cho một hệ thống tích hợp. Quy tắc chuẩn bị dữ liệu nên nằm ở một chỗ khi có thêm định dạng.

## Mẫu thiết kế và ranh giới

Creator cơ sở `ExportJob` quản lý thao tác chung `run()`. Thao tác này gọi `createWriter()`, phương thức mà lớp con có thể ghi đè, rồi dùng đối tượng trả về qua interface `ReportWriter`. Mỗi lớp tác vụ quyết định khởi tạo writer nào. Route hoặc mã khởi tạo ứng dụng chọn loại tác vụ. Writer xử lý dữ liệu đã chuẩn bị mà không phụ thuộc vào các bước còn lại.

## Ví dụ TypeScript

Cả hai tác vụ nhận cùng một tập dữ liệu chưa chuẩn hóa. Các phép kiểm tra xác nhận nội dung và kiểu nội dung của từng kết quả. Writer văn bản tạo định dạng hiển thị đơn giản với mỗi nhãn trên một dòng. Dùng định dạng có cấu trúc như JSON nếu nhãn có thể chứa ký tự xuống dòng và cần khôi phục nguyên vẹn sau khi đọc.

```typescript
type ReportRow = Readonly<{ label: string }>
type ReportFile = Readonly<{ mediaType: string; body: string }>

interface ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile
}

class TextReportWriter implements ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile {
    return {
      mediaType: "text/plain",
      body: rows.map(row => row.label).join("\n"),
    }
  }
}

class JsonReportWriter implements ReportWriter {
  write(rows: readonly ReportRow[]): ReportFile {
    return { mediaType: "application/json", body: JSON.stringify(rows) }
  }
}

abstract class ExportJob {
  protected abstract createWriter(): ReportWriter

  run(rows: readonly ReportRow[]): ReportFile {
    const normalized = rows.map(row => ({ label: row.label.trim() }))
    return this.createWriter().write(normalized)
  }
}

class TextExportJob extends ExportJob {
  protected createWriter(): ReportWriter {
    return new TextReportWriter()
  }
}

class JsonExportJob extends ExportJob {
  protected createWriter(): ReportWriter {
    return new JsonReportWriter()
  }
}

const rows = [{ label: " Purchase " }, { label: "Travel " }]
const textFile = new TextExportJob().run(rows)
if (textFile.mediaType !== "text/plain" || textFile.body !== "Purchase\nTravel") {
  throw new Error("Text export must contain both normalized labels")
}

const jsonFile = new JsonExportJob().run(rows)
if (jsonFile.mediaType !== "application/json" ||
    jsonFile.body !== '[{"label":"Purchase"},{"label":"Travel"}]') {
  throw new Error("JSON export must encode the same normalized rows")
}
```

## Khi nên dùng

Dùng Factory Method khi lớp cơ sở đã quản lý một luồng lặp lại và cần để lớp con chọn đối tượng cộng tác mà luồng sẽ tạo. Dấu hiệu dễ thấy là loại product mới nào cũng buộc sửa luồng đã ổn định. Giữ phương thức khởi tạo đủ hẹp để thao tác cơ sở áp dụng được cùng một hợp đồng cho mọi product.

### Bài toán thường gặp

- **Xuất báo cáo theo định dạng.** Luồng chung chọn dữ liệu, chuẩn hóa và trả kết quả. Lớp xuất CSV và lớp xuất JSON chỉ ghi đè phương thức tạo bộ ghi. Khi thêm một định dạng, logic chuẩn hóa vẫn ở lớp cơ sở.
- **Nhập hồ sơ từ tệp khác nhau.** Lớp nhập chung quản lý việc đọc bản ghi, kiểm tra hợp lệ và báo lỗi. Mỗi lớp con tạo bộ phân tích CSV hoặc bảng tính theo cùng giao diện đọc bản ghi. Một hàm nhận bộ phân tích làm tham số thường đủ khi không có sẵn hệ lớp dùng chung.

## Khi cách đơn giản đã đủ

Một hàm chọn writer theo định dạng là đủ khi danh sách định dạng cố định. Nếu bên gọi truyền vào được writer hoặc hàm khởi tạo writer, constructor injection cho phép tái dùng luồng với ít lớp hơn. Phương thức tĩnh `fromFormat(format)` là một factory có tên với logic lựa chọn nằm trong chính phương thức đó.

## Đánh đổi

- Thiết kế này cần một creator cụ thể cho mỗi writer mới. Hệ phân cấp creator sâu khiến việc lần ra đối tượng thực sự chạy trong production khó hơn.
- Có thể kiểm thử từng biến thể qua luồng public. Phần chuẩn hóa vẫn cần phép kiểm tra chung vì ảnh hưởng đến mọi writer.
- Quy định rõ bên nào quản lý vòng đời của product tốn tài nguyên. Ví dụ tạo một writer không giữ trạng thái ở mỗi lượt chạy nên vòng đời của writer nằm trong lượt đó.

## Bài tập

Thêm writer xuất JSON theo từng dòng và lớp tác vụ tương ứng. Kiểm tra kiểu nội dung và xác nhận hai dòng đầu vào sinh hai dòng JSON có thể phân tích riêng, với nhãn đã bỏ khoảng trắng thừa. Giữ nguyên `ExportJob.run()`.

## Tài liệu tham khảo

- [Refactoring.Guru · Factory Method](https://refactoring.guru/design-patterns/factory-method)

[Chương sau → · 02. Abstract Factory](02-abstract-factory.md)
