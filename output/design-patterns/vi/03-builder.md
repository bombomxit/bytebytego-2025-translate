# 03. Builder

[Mục lục](../README.md) · [English](../original/03-builder.md)

## Bài toán

Nhóm quản lý tài liệu chuẩn bị một gói phát hành gồm tiêu đề, tóm tắt tùy chọn và checklist có thứ tự. Cùng một gói được biểu diễn dưới dạng dữ liệu có cấu trúc cho hệ thống tự động và văn bản thuần cho người rà soát. Cả hai đầu ra phải tuân thủ cùng quy tắc về thứ tự và độ đầy đủ. Khi có thêm mục tùy chọn, lắp ráp riêng cho từng đầu ra dễ làm sót bước.

## Mẫu thiết kế và ranh giới

Interface `PackageBuilder` quy định các bước lắp ráp. `assemblePackage()` đóng vai trò director, áp dụng cùng một trình tự cho cả hai builder. `StructuredPackageBuilder` và `TextPackageBuilder` quyết định cách biểu diễn từng bước và cung cấp cách lấy kết quả riêng. Director giữ trình tự lắp ráp, builder giữ cách biểu diễn, còn bên gọi tạo builder mới cho mỗi kết quả.

## Ví dụ TypeScript

Ví dụ kiểm tra hai builder giữ đúng thứ tự checklist và quy trình chung từ chối checklist rỗng. Builder có cấu trúc sao chép checklist khi trả về, để kết quả có mảng riêng.

```typescript
type PackageDraft = Readonly<{
  title: string
  summary?: string
  checks: readonly string[]
}>

interface PackageBuilder {
  setTitle(title: string): void
  setSummary(summary: string): void
  addCheck(check: string): void
}

function assemblePackage(draft: PackageDraft, builder: PackageBuilder): void {
  if (!draft.title.trim() || draft.checks.length === 0) {
    throw new Error("A title and at least one check are required")
  }

  builder.setTitle(draft.title)
  if (draft.summary) builder.setSummary(draft.summary)
  for (const check of draft.checks) builder.addCheck(check)
}

class StructuredPackageBuilder implements PackageBuilder {
  private title = ""
  private summary: string | undefined
  private readonly checks: string[] = []

  setTitle(title: string): void {
    this.title = title
  }

  setSummary(summary: string): void {
    this.summary = summary
  }

  addCheck(check: string): void {
    this.checks.push(check)
  }

  build(): PackageDraft {
    return {
      title: this.title,
      ...(this.summary === undefined ? {} : { summary: this.summary }),
      checks: [...this.checks],
    }
  }
}

class TextPackageBuilder implements PackageBuilder {
  private readonly lines: string[] = []

  setTitle(title: string): void {
    this.lines.push(title)
  }

  setSummary(summary: string): void {
    this.lines.push(summary)
  }

  addCheck(check: string): void {
    this.lines.push("- " + check)
  }

  build(): string {
    return this.lines.join("\n")
  }
}

const draft = {
  title: "Policy update",
  summary: "Review before Friday",
  checks: ["Confirm dates", "Notify staff"],
}
const structured = new StructuredPackageBuilder()
const textBuilder = new TextPackageBuilder()
assemblePackage(draft, structured)
assemblePackage(draft, textBuilder)
const result = structured.build()
if (result.title !== draft.title || result.summary !== draft.summary ||
    result.checks.join(",") !== "Confirm dates,Notify staff") {
  throw new Error("The structured package must preserve the draft")
}
if (textBuilder.build() !== "Policy update\nReview before Friday\n- Confirm dates\n- Notify staff") {
  throw new Error("The text package must preserve the recipe order")
}

let rejected = false
try {
  assemblePackage({ title: draft.title, checks: [] }, new TextPackageBuilder())
} catch (error) {
  rejected = error instanceof Error && error.message === "A title and at least one check are required"
}
if (!rejected) throw new Error("The recipe must reject an empty checklist")
```

## Khi nên dùng

Dùng Builder khi phải lắp đối tượng qua nhiều bước hoặc khi một trình tự lắp ráp có thể tạo nhiều cách biểu diễn. Xác định các tổ hợp hợp lệ và chỉ cho lấy kết quả sau khi các điều kiện của luồng khởi tạo tương ứng đã được đáp ứng. Director hữu ích khi nhiều bên gọi dùng chung trình tự.

### Bài toán thường gặp

- **Cấu hình báo cáo định kỳ.** Người dùng chọn nguồn dữ liệu, bộ lọc, định dạng và lịch gửi qua nhiều bước. Builder gom các lựa chọn và chỉ tạo cấu hình cuối khi có đủ trường bắt buộc, chẳng hạn lịch gửi phải có múi giờ.
- **Dựng bộ hồ sơ xuất.** Quy trình có thể gắn nhiều tài liệu, thêm mục lục và bật mã hóa. Builder kiểm tra tổ hợp ở bước hoàn tất, chẳng hạn hồ sơ bật mã hóa phải có người nhận hợp lệ. Nếu toàn bộ tham số đã có ngay và chỉ cần kiểm tra một lần, hàm tạo nhận một đối tượng cấu hình có thể đủ.

## Khi cách đơn giản đã đủ

Bắt đầu với một đối tượng tùy chọn có kiểu và một hàm kiểm tra nếu mọi trường đã sẵn sàng cùng lúc và chỉ có một cách biểu diễn. Nếu hai đầu ra chỉ là cách tuần tự hóa khác nhau của một domain object hoàn chỉnh và ổn định, hãy khởi tạo đối tượng một lần rồi viết hai serializer. Builder có ích khi từng đầu ra có thêm bước xử lý tăng dần hoặc phụ thuộc thứ tự.

## Đánh đổi

- Builder có trạng thái thay đổi nên cần quản lý vòng đời. Ví dụ dùng một builder mới cho mỗi gói. Dùng lại mà quên reset có thể trộn checklist của nhiều gói.
- Interface chung giúp tái dùng trình tự lắp ráp. Nếu thêm bước bắt buộc vào trình tự, có thể phải sửa tất cả builder cụ thể.
- Trình tự chung kiểm tra đường gọi thông thường. Kiểm tra hoặc giới hạn cả các lời gọi trực tiếp nếu sản phẩm phải giữ cùng ràng buộc với mọi bên gọi.

## Bài tập

Thêm ghi chú tùy chọn của người rà soát sau phần tóm tắt. Kiểm tra builder văn bản đặt ghi chú trước mục đầu tiên của checklist và builder có cấu trúc chỉ đưa ghi chú vào khi được cung cấp.

## Tài liệu tham khảo

- [Refactoring.Guru · Builder](https://refactoring.guru/design-patterns/builder)

[← Chương trước · 02. Abstract Factory](02-abstract-factory.md) · [Chương sau → · 04. Prototype](04-prototype.md)
