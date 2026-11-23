# 12. Proxy

[Mục lục](../README.md) · [English](../original/12-proxy.md)

## Bài toán

Duyệt metadata tài liệu hiếm khi cần danh mục bản xem trước, nhưng mở chỉ mục xem trước cục bộ có thể tốn tài nguyên. Interface tra cứu đã tồn tại và các tính năng dùng nó trong toàn ứng dụng. Nếu nạp ngay khi khởi tạo, mọi tiến trình đều phải trả chi phí đó. Nếu mỗi bên gọi tự nạp khi cần, trách nhiệm giữ danh mục và xử lý lỗi khởi tạo sẽ rải rác qua các tính năng.

## Mẫu thiết kế và ranh giới

Proxy đóng vai trò đại diện cho đối tượng đích và kiểm soát cách thức hoặc thời điểm truy cập nó. `PreviewCatalog` là interface chung, `LoadedPreviewCatalog` là đối tượng đích, còn `LazyPreviewCatalog` là virtual proxy nạp đối tượng đích ở lần tra cứu đầu tiên. Bên gọi chỉ thấy hợp đồng tra cứu. Trong thiết kế Decorator, bên gọi thường ghép các trách nhiệm tùy chọn quanh một thành phần đã có. Ở đây proxy quản lý đường truy cập instance thật và quyết định khi nào nó được tạo.

## Ví dụ TypeScript

Các kiểm tra cho thấy tạo proxy chưa nạp danh mục. Lần tra cứu đầu tiên nạp danh mục. Các lượt sau dùng lại cùng instance và giữ nguyên kết quả khi không có mục tương ứng.

```typescript
interface PreviewCatalog {
  lookup(documentId: string): string | undefined;
}

class LoadedPreviewCatalog implements PreviewCatalog {
  constructor(private readonly files: ReadonlyMap<string, string>) {}

  lookup(documentId: string): string | undefined {
    return this.files.get(documentId);
  }
}

class LazyPreviewCatalog implements PreviewCatalog {
  private catalog?: PreviewCatalog;

  constructor(private readonly load: () => PreviewCatalog) {}

  lookup(documentId: string): string | undefined {
    if (this.catalog === undefined) {
      this.catalog = this.load();
    }
    return this.catalog.lookup(documentId);
  }
}

let loadCount = 0;
const catalog: PreviewCatalog = new LazyPreviewCatalog(() => {
  loadCount += 1;
  return new LoadedPreviewCatalog(new Map([["d1", "preview-d1.webp"]]));
});
const initialLoadCount = loadCount;
if (initialLoadCount !== 0 || catalog.lookup("d1") !== "preview-d1.webp") {
  throw new Error("The real catalog should load only at first use");
}

if (catalog.lookup("unknown") !== undefined || loadCount !== 1) {
  throw new Error("Repeated lookups should reuse the catalog and preserve misses");
}
```

## Khi nên dùng

Dùng khi đối tượng đích tốn tài nguyên để khởi tạo và bên gọi cần interface ổn định. Các cách dùng quen thuộc khác gồm đối tượng đại diện cho một đối tượng từ xa hoặc protection proxy kiểm tra quyền ở ranh giới tin cậy. Với mỗi cách dùng, hãy quy định rõ bên gọi nhận được gì khi thành công và khi lỗi.

### Bài toán thường gặp

- **Trì hoãn tải bản xem trước.** Giao diện hiển thị thông tin tài liệu trước, còn đối tượng đại diện chỉ mở tài nguyên khi người dùng yêu cầu xem. Với tải bất đồng bộ, nhiều lượt xem đồng thời có thể dùng chung một yêu cầu đang chạy. Quy định lúc được thử lại nếu lần tải đầu thất bại.
- **Đại diện cho dịch vụ từ xa.** Bên gọi dùng đối tượng đại diện qua cùng giao diện của dịch vụ. Đối tượng này gửi lời gọi qua mạng và báo lỗi hết thời gian chờ khi cần. Hợp đồng nên mô tả rõ lỗi mạng và điều kiện gọi lại an toàn vì một lệnh từ xa có thể đã chạy trước khi mất phản hồi.

## Khi cách đơn giản đã đủ

Nếu khởi tạo rẻ hoặc tiến trình nào cũng cần danh mục ngay, hãy tạo đối tượng thật trực tiếp. Nếu chỉ có một bên gọi, getter nạp khi cần hoặc một thao tác nạp rõ ràng tại chỗ dùng có thể đủ để quản lý vòng đời.

## Đánh đổi

Trì hoãn nạp chuyển chi phí và lỗi khởi tạo sang yêu cầu đầu tiên. Trong ví dụ đồng bộ, nếu thao tác nạp ném lỗi thì danh mục vẫn chưa được gán. Lượt tra cứu sau sẽ thử nạp lại. Proxy bất đồng bộ nên chia sẻ lần nạp đang chạy khi phù hợp, đồng thời quy định cách thử lại và hủy. Nếu đối tượng đích có thể thay đổi, proxy cần vòng đời hoặc chính sách vô hiệu hóa rõ ràng.

## Bài tập

Cho loader ném lỗi ở lần đầu và thành công ở lần thứ hai. Kiểm tra lần tra cứu đầu nhận lỗi, lần thứ hai có thể thành công và lần thứ ba không nạp lại.

## Tài liệu tham khảo

- [Proxy — Refactoring.Guru](https://refactoring.guru/design-patterns/proxy)

[← Chương trước · 11. Flyweight](11-flyweight.md) · [Chương sau → · 13. Chain of Responsibility](13-chain-of-responsibility.md)
