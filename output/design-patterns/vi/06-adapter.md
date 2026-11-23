# 06. Adapter

[Mục lục](../README.md) · [English](../original/06-adapter.md)

## Bài toán

Cổng tài liệu cần đọc metadata từ một hệ thống chỉ mục cũ. Màn hình và tác vụ nền cần mã tài liệu, kích thước theo byte và cách phân biệt giữa tài liệu vắng mặt với sự cố chỉ mục. Hệ thống cũ có tên trường và mã trạng thái riêng. Nếu bên gọi nào cũng tự diễn giải chúng, mỗi lần thay chỉ mục phải tìm và sửa từng chỗ chuyển đổi. Nếu sự cố bị hiểu thành tài liệu vắng mặt, hệ thống còn có thể gửi nhầm thông báo “tài liệu đã bị xóa”.

## Mẫu thiết kế và ranh giới

Adapter triển khai interface mà bên gọi đang cần rồi ủy quyền cho dịch vụ có giao diện khác. Trong ví dụ, `DocumentDirectory` là interface đích, `LegacyIndex` là dịch vụ được thích nghi, còn `LegacyDirectoryAdapter` chịu trách nhiệm chuyển đổi. Bên gọi chỉ phụ thuộc hợp đồng của danh mục và có thể nhận adapter cũ hoặc bản thay thế. Giữ ranh giới hẹp để các quy ước riêng của nhà cung cấp nằm trong adapter. Chính sách như thử lại truy vấn thuộc về bên gọi phù hợp hoặc lớp xử lý khả năng phục hồi.

## Ví dụ TypeScript

Kiểu phản hồi từ chỉ mục cũ mô tả dữ liệu đã được giải mã. Adapter chuyển đổi các trường và mã trạng thái. Hai kiểm tra xác nhận metadata được chuẩn hóa và vẫn phân biệt được sự cố chỉ mục với tài liệu vắng mặt.

```typescript
type DocumentInfo = { id: string; bytes: number };
type DocumentLookup =
  | { kind: "found"; document: DocumentInfo }
  | { kind: "missing" }
  | { kind: "unavailable" };

interface DocumentDirectory {
  find(id: string): DocumentLookup;
}

type LegacyReply =
  | { status: "OK"; record: { document_no: string; size_b: number } }
  | { status: "NOT_FOUND" }
  | { status: "INDEX_OFFLINE" };

interface LegacyIndex {
  lookup(documentNumber: string): LegacyReply;
}

class LegacyDirectoryAdapter implements DocumentDirectory {
  constructor(private readonly legacy: LegacyIndex) {}

  find(id: string): DocumentLookup {
    const reply = this.legacy.lookup(id);
    switch (reply.status) {
      case "OK":
        return {
          kind: "found",
          document: { id: reply.record.document_no, bytes: reply.record.size_b },
        };
      case "NOT_FOUND":
        return { kind: "missing" };
      case "INDEX_OFFLINE":
        return { kind: "unavailable" };
    }
  }
}

const directory: DocumentDirectory = new LegacyDirectoryAdapter({
  lookup: (id) => {
    if (id === "d1") {
      return { status: "OK", record: { document_no: id, size_b: 240 } };
    }
    if (id === "d2") return { status: "NOT_FOUND" };
    return { status: "INDEX_OFFLINE" };
  },
});
const found = directory.find("d1");
if (found.kind !== "found" || found.document.id !== "d1" ||
    found.document.bytes !== 240) {
  throw new Error("Expected normalized document metadata");
}
if (directory.find("d2").kind !== "missing" ||
    directory.find("d3").kind !== "unavailable") {
  throw new Error("Missing documents and outages must stay distinct");
}
```

## Khi nên dùng

Dùng khi nhiều bên gọi phải hiểu cùng một quy ước riêng của nhà cung cấp, hoặc khi cần chạy đồng thời tích hợp cũ và mới dưới một hợp đồng ứng dụng. Trong ví dụ, nhà cung cấp thứ hai có thể trả về cùng kiểu union từ một phản hồi khác mà không cần sửa cổng tài liệu hay tác vụ nền.

## Khi cách đơn giản đã đủ

Nếu chỉ đổi tên một trường sau một request tại một chỗ, hàm ánh xạ cục bộ có thể đủ. Adapter dạng đối tượng có ích khi ứng dụng cần một dependency ổn định với nhiều cách triển khai, cần quản lý vòng đời, hoặc có nhiều thao tác dùng cùng một nhà cung cấp.

## Đánh đổi

Cần bảo trì phần chuyển đổi khi ý nghĩa dữ liệu từ hệ thống nguồn đổi. Hợp đồng nên ghi rõ đơn vị, khả năng nhận giá trị null và ý nghĩa lỗi. Kiểu dữ liệu khớp nhau vẫn có thể mang nghĩa khác nhau. Tại ranh giới mạng thật, cần kiểm tra payload sau khi giải mã và quy định cách báo phản hồi sai định dạng hoặc lỗi kết nối.

## Bài tập

Viết adapter cho chỉ mục thay thế trả kích thước theo KiB. Chạy lại các kiểm tra qua `DocumentDirectory` và thêm ca 2 KiB được đổi thành 2048 byte. Giữ nguyên bên gọi.

## Tài liệu tham khảo

- [Adapter — Refactoring.Guru](https://refactoring.guru/design-patterns/adapter)

[← Chương trước · 05. Singleton](05-singleton.md) · [Chương sau → · 07. Bridge](07-bridge.md)
