# 10. Facade

[Mục lục](../README.md) · [English](../original/10-facade.md)

## Bài toán

Endpoint xuất tài liệu và một worker nền cùng cần chuẩn bị phiên bản tài liệu mới nhất để gửi đi nếu phiên bản đó đã được duyệt. Mỗi yêu cầu đọc phiên bản, kiểm tra trạng thái, kết xuất đúng nội dung vừa đọc và lưu kết quả theo số phiên bản đó. Viết lại chuỗi thao tác ở nhiều nơi dễ làm hành vi lệch nhau. Nếu worker kết xuất bản nháp hoặc lưu đầu ra dưới số phiên bản mới hơn, hệ thống có thể không truy vết được dữ liệu dùng để tạo bản xuất.

## Mẫu thiết kế và ranh giới

Facade cung cấp một điểm vào cho nhiều thao tác của các hệ thống con. Bên gọi truyền mã tài liệu vào `DocumentExport.prepare`. Facade điều phối `VersionStore`, `ExportRenderer` và `ExportArchive` rồi trả kết quả ở cấp ứng dụng. Interface của từng hệ thống con vẫn phục vụ được các ca sử dụng riêng. Ví dụ, dịch vụ xem trước có thể dùng renderer mà không gọi kho lưu bản xuất. Giữ facade tập trung vào thao tác xuất và để logic lưu trữ, kết xuất chung ở các thành phần phụ trách.

## Ví dụ TypeScript

Các kiểm tra cho thấy bản đã duyệt đi qua ba dependency theo đúng thứ tự, còn bản nháp dừng trước khi kết xuất hay lưu. Dependency trong bộ nhớ ghi lại những gì đã diễn ra để ví dụ chạy được mà không cần hạ tầng.

```typescript
type Version = { revision: number; approved: boolean; text: string };

interface VersionStore {
  latest(documentId: string): Version;
}

interface ExportRenderer {
  render(text: string): string;
}

interface ExportArchive {
  store(documentId: string, revision: number, output: string): string;
}

type ExportResult =
  | { kind: "ready"; archiveId: string }
  | { kind: "approval-required" };

class DocumentExport {
  constructor(
    private readonly versions: VersionStore,
    private readonly renderer: ExportRenderer,
    private readonly archive: ExportArchive,
  ) {}

  prepare(documentId: string): ExportResult {
    const version = this.versions.latest(documentId);
    if (!version.approved) return { kind: "approval-required" };

    const output = this.renderer.render(version.text);
    const archiveId = this.archive.store(documentId, version.revision, output);
    return { kind: "ready", archiveId };
  }
}

const trace: string[] = [];
const exporter = new DocumentExport(
  {
    latest: (documentId) => {
      trace.push("read:" + documentId);
      return { revision: 3, approved: documentId === "approved", text: "Summary" };
    },
  },
  {
    render: (text) => {
      trace.push("render:" + text);
      return "Exported " + text;
    },
  },
  {
    store: (documentId, revision, output) => {
      trace.push("store:" + output);
      return documentId + "/" + revision;
    },
  },
);

const ready = exporter.prepare("approved");
if (ready.kind !== "ready" || ready.archiveId !== "approved/3") {
  throw new Error("The facade should return the archived revision");
}
if (exporter.prepare("draft").kind !== "approval-required" ||
    trace.join(",") !== "read:approved,render:Summary,store:Exported Summary,read:draft") {
  throw new Error("A draft should stop before rendering and archiving");
}
```

## Khi nên dùng

Dùng khi bên gọi cần một thao tác ổn định gồm nhiều lời gọi hoặc quy tắc ở mức thấp hơn. Endpoint xuất tài liệu trên mobile và worker có thể dùng chung hợp đồng ngay cả khi cách lưu trữ hay kết xuất thay đổi. Nếu interface của nhà cung cấp không tương thích, facade có thể dùng adapter làm một thành phần.

## Khi cách đơn giản đã đủ

Nếu một bên gọi chỉ gọi một thao tác ổn định, dùng hệ thống con trực tiếp. Một hàm nhỏ có thể đủ để điều phối hai lời gọi thuộc cùng module. Tách facade khi ca sử dụng cần một ranh giới rõ ràng và nhiều bên gọi có thể dùng chung ranh giới đó.

## Đánh đổi

Bên gọi thấy ít chi tiết triển khai hơn nên kết quả phải cho biết bước tiếp theo có thể làm. Quy định hành vi khi lưu lỗi và khi thử lại trước khi dùng facade trong worker. Quá trình tải lên có thể thành công nhưng phản hồi bị mất. Để thử lại an toàn, có thể cần khóa idempotency lưu bền vững theo tài liệu, phiên bản và định dạng xuất.

## Bài tập

Mở rộng ví dụ với một renderer ném lỗi. Kiểm tra lỗi được truyền ra và kho lưu bản xuất chưa bị gọi. Giữ nguyên chữ ký của facade và các bên gọi.

## Tài liệu tham khảo

- [Facade — Refactoring.Guru](https://refactoring.guru/design-patterns/facade)

[← Chương trước · 09. Decorator](09-decorator.md) · [Chương sau → · 11. Flyweight](11-flyweight.md)
