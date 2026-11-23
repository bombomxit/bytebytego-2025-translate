# 07. Bridge

[Mục lục](../README.md) · [English](../original/07-bridge.md)

## Bài toán

Cổng vận hành xuất báo cáo dung lượng và báo cáo hàng chờ duyệt. Cả hai cần Markdown cho người đọc và JSON cho tác vụ thu thập định kỳ. Nếu tạo một lớp con cho từng tổ hợp, nội dung sẽ bị gắn với định dạng tệp. Thêm một báo cáo đồng nghĩa với thêm một lớp cho mỗi định dạng đang hỗ trợ. Thêm một định dạng lại lặp công việc trên các báo cáo hiện có. Hai nhóm thay đổi thuộc các đội phụ trách và lịch phát hành khác nhau.

## Mẫu thiết kế và ranh giới

Bridge nối hai nhóm có thể thay đổi độc lập bằng composition. Lớp trừu tượng `Report` định nghĩa thao tác xuất, còn mỗi loại báo cáo cung cấp tiêu đề và các dòng dữ liệu. `ReportRenderer` là interface mô tả khả năng kết xuất ở mức thấp hơn. Các renderer cụ thể mã hóa cùng cấu trúc báo cáo theo những định dạng khác nhau. Bên gọi chọn một loại báo cáo và một renderer. Báo cáo ủy quyền định dạng qua interface đó. Trong ví dụ, hợp đồng giữa hai phía gồm tiêu đề và danh sách dòng, mỗi dòng có nhãn và giá trị số.

## Ví dụ TypeScript

Ví dụ kiểm tra cả bốn cách ghép hai báo cáo với hai renderer. Mỗi báo cáo khai báo nội dung một lần. Đổi định dạng thì sửa renderer tương ứng, còn đổi phép tính thì sửa báo cáo tương ứng.

```typescript
type ReportRow = readonly [label: string, value: number];

interface ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string;
}

abstract class Report {
  constructor(private readonly renderer: ReportRenderer) {}
  protected abstract title(): string;
  protected abstract rows(): readonly ReportRow[];

  export(): string {
    return this.renderer.render(this.title(), this.rows());
  }
}

class StorageReport extends Report {
  protected title(): string {
    return "Storage";
  }

  protected rows(): readonly ReportRow[] {
    return [["Used bytes", 1200]];
  }
}

class ReviewReport extends Report {
  protected title(): string {
    return "Review queue";
  }

  protected rows(): readonly ReportRow[] {
    return [["Pending", 3]];
  }
}

class MarkdownRenderer implements ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string {
    return ["# " + title, ...rows.map(([label, value]) => "- " + label + ": " + value)]
      .join("\n");
  }
}

class JsonRenderer implements ReportRenderer {
  render(title: string, rows: readonly ReportRow[]): string {
    return JSON.stringify({ title, rows });
  }
}

const markdown = new MarkdownRenderer();
const json = new JsonRenderer();

if (new StorageReport(markdown).export() !== "# Storage\n- Used bytes: 1200" ||
    new ReviewReport(markdown).export() !== "# Review queue\n- Pending: 3") {
  throw new Error("Both report types should work with Markdown");
}
if (new StorageReport(json).export() !== '{"title":"Storage","rows":[["Used bytes",1200]]}' ||
    new ReviewReport(json).export() !== '{"title":"Review queue","rows":[["Pending",3]]}') {
  throw new Error("Both report types should work with JSON");
}
```

## Khi nên dùng

Dùng Bridge khi cả hai chiều đã có biến thể hoặc chiều thứ hai có kế hoạch thay đổi cụ thể. Tìm các tổ hợp có chung một hợp đồng thực sự. Chẳng hạn, renderer văn bản thuần mới nên biểu diễn được các báo cáo hiện có từ cùng tiêu đề và các dòng dữ liệu.

## Khi cách đơn giản đã đủ

Một báo cáo với một định dạng ổn định có thể dùng một hàm. Truyền một hàm định dạng làm tham số cũng có thể đủ nếu chỉ định dạng thay đổi và các báo cáo chưa có thao tác chung. Tách interface có tên khi hai chiều cần hợp đồng ổn định và cách triển khai riêng.

## Đánh đổi

Hợp đồng chung cần được thiết kế và duy trì. Báo cáo chỉ có biểu đồ hoặc định dạng có yêu cầu khác về độ trung thực có thể buộc cả hai phía phải đổi. Hãy kiểm tra các tổ hợp thật và mô hình hóa rõ những khả năng bắt buộc. Khi sửa interface, đánh giá chi phí trên từng báo cáo và renderer hiện có.

## Bài tập

Thêm `PlainTextRenderer` để xuất tiêu đề ở dòng đầu và mỗi dòng dữ liệu theo dạng `label=value`. Kiểm tra cả hai báo cáo với renderer mới và giữ nguyên hai lớp báo cáo.

## Tài liệu tham khảo

- [Bridge — Refactoring.Guru](https://refactoring.guru/design-patterns/bridge)

[← Chương trước · 06. Adapter](06-adapter.md) · [Chương sau → · 08. Composite](08-composite.md)
