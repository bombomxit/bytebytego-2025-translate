# 09. Decorator

[Mục lục](../README.md) · [English](../original/09-decorator.md)

## Bài toán

Dịch vụ tài liệu đọc dữ liệu từ thành phần lưu trữ hiện có. Một số điểm vào cần ghi sự kiện sau mỗi lượt đọc thành công, còn đội vận hành cần đếm mọi lượt gọi, kể cả khi lỗi. Ứng dụng có thể bật từng hành vi độc lập. Nếu bộ đọc có một cờ cho mỗi trách nhiệm, mã đọc nội dung phải xử lý mọi cách kết hợp. Khi thêm backend lưu trữ thứ hai, phần xử lý đó cũng có thể bị sao chép.

## Mẫu thiết kế và ranh giới

Decorator bọc một thành phần, triển khai cùng interface với bên gọi và thêm hành vi quanh thao tác ủy quyền. `MemoryReader` là thành phần cụ thể. `ReadAudit` và `ReadMetrics` là các decorator, mỗi lớp nhận một `DocumentReader`, có thể là một decorator khác. Bên gọi vẫn dùng cùng interface. Hai lớp bọc có thể thay đổi độc lập với bộ đọc và được ghép tại chỗ khởi tạo dependency của ứng dụng.

## Ví dụ TypeScript

Ví dụ ghi lượt đọc thành công vào danh sách sự kiện trong bộ nhớ và đếm tổng lượt gọi. Các kiểm tra bao quát giá trị trả về ban đầu, việc truyền nguyên lỗi của bộ đọc và ý nghĩa riêng của hai phép đo.

```typescript
interface DocumentReader {
  read(id: string): string;
}

class MemoryReader implements DocumentReader {
  constructor(private readonly docs: ReadonlyMap<string, string>) {}

  read(id: string): string {
    const body = this.docs.get(id);
    if (body === undefined) throw new Error("Unknown document");
    return body;
  }
}

class ReadAudit implements DocumentReader {
  constructor(
    private readonly inner: DocumentReader,
    private readonly events: string[],
  ) {}

  read(id: string): string {
    const body = this.inner.read(id);
    this.events.push("read:" + id);
    return body;
  }
}

class ReadMetrics implements DocumentReader {
  attempts = 0;

  constructor(private readonly inner: DocumentReader) {}

  read(id: string): string {
    this.attempts += 1;
    return this.inner.read(id);
  }
}

const events: string[] = [];
const base = new MemoryReader(new Map([["a", "meeting notes"]]));
const metrics = new ReadMetrics(new ReadAudit(base, events));
const reader: DocumentReader = metrics;
if (reader.read("a") !== "meeting notes" || events.join(",") !== "read:a") {
  throw new Error("The decorated reader should retain the base result");
}

let missing = false;
try {
  reader.read("missing");
} catch (error) {
  if (!(error instanceof Error) || error.message !== "Unknown document") throw error;
  missing = true;
}
if (!missing || metrics.attempts !== 2 || events.length !== 1) {
  throw new Error("Count both attempts and record only successful reads");
}
```

## Khi nên dùng

Dùng khi các bên gọi có chung interface ổn định và cần ghép những trách nhiệm tùy chọn theo từng tổ hợp. Với cùng hợp đồng đọc, lớp ghi sự kiện có thể bọc bộ đọc từ hệ thống tệp hoặc cổng lưu trữ. Nếu framework đã có middleware hay interceptor ở đúng ranh giới, chúng có thể đáp ứng cách ghép này.

## Khi cách đơn giản đã đủ

Một quy tắc luôn áp dụng có thể đặt trong thành phần hoặc tại bên gọi duy nhất. Hàm bậc cao cũng có thể đủ nếu interface chỉ có một hàm và mỗi instance không cần cấu hình hoặc trạng thái riêng.

## Đánh đổi

Thứ tự bọc quyết định hành động nào được quan sát và khi nào hiệu ứng phụ xảy ra. Chẳng hạn, đặt lớp đo ở ngoài cache sẽ đếm mọi lượt đọc, còn đặt bên trong chỉ đếm lượt chạm kho lưu trữ. Quy định cách xử lý lỗi của đích ghi log hoặc chỉ số, nhất là khi thao tác chỉ được công nhận thành công nếu có bản ghi kiểm toán. Kiểm tra những tổ hợp phụ thuộc các quy ước đó.

## Bài tập

Thêm lớp bọc ghi độ dài nội dung đọc thành công rồi ghép với hai decorator hiện có. Kiểm tra khi tài liệu vắng mặt, lỗi ban đầu vẫn được truyền ra và hệ thống không ghi độ dài hay sự kiện thành công.

## Tài liệu tham khảo

- [Decorator — Refactoring.Guru](https://refactoring.guru/design-patterns/decorator)

[← Chương trước · 08. Composite](08-composite.md) · [Chương sau → · 10. Facade](10-facade.md)
