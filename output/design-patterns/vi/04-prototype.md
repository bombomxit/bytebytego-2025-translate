# 04. Prototype

[Mục lục](../README.md) · [English](../original/04-prototype.md)

## Bài toán

Cổng nội bộ tạo quy trình rà soát theo mẫu có sẵn của từng phòng ban. Mỗi mẫu đã có tên các bước và danh sách người rà soát mặc định. Bản nháp mới cần bắt đầu từ cấu hình đó và vẫn cho phép chỉnh sửa. Nếu bản nháp dùng chung một danh sách có thể thay đổi với mẫu, thao tác thêm người rà soát sẽ âm thầm làm đổi cấu hình của tài liệu tiếp theo.

## Mẫu thiết kế và ranh giới

Prototype đưa quy tắc sao chép vào thao tác `clone()`. `startReview()` yêu cầu `ReviewPrototype` đã chọn tạo bản nháp mới. Mẫu cụ thể biết trường nào cần sao chép riêng và đặt tên mới cho bản nháp trong khi giữ cấu hình các bước. Khi có thêm những kiểu mẫu độc lập, mỗi kiểu giữ được quy tắc riêng mà bên gọi không cần thêm nhánh để dựng lại đối tượng.

## Ví dụ TypeScript

Constructor sở hữu trạng thái có thể thay đổi bằng cách sao chép các bước và danh sách người rà soát bên trong từng bước. `clone()` gọi constructor này nên hai bản nháp bắt đầu với cùng giá trị và có thể sửa độc lập. Ví dụ kiểm tra các giá trị kế thừa và khả năng chỉnh sửa riêng của hai bản nháp.

```typescript
type ReviewStage = Readonly<{ name: string; reviewers: readonly string[] }>

interface ReviewDraft {
  readonly name: string
  addReviewer(stageName: string, reviewer: string): void
  reviewersFor(stageName: string): readonly string[]
}

interface ReviewPrototype {
  clone(draftName: string): ReviewDraft
}

class ReviewWorkflow implements ReviewPrototype, ReviewDraft {
  private readonly stages: { name: string; reviewers: string[] }[]

  constructor(readonly name: string, stages: readonly ReviewStage[]) {
    this.stages = stages.map(stage => ({
      name: stage.name,
      reviewers: [...stage.reviewers],
    }))
  }

  clone(draftName: string): ReviewWorkflow {
    return new ReviewWorkflow(draftName, this.stages)
  }

  addReviewer(stageName: string, reviewer: string): void {
    const stage = this.stages.find(candidate => candidate.name === stageName)
    if (!stage) throw new Error("Unknown review stage")
    stage.reviewers.push(reviewer)
  }

  reviewersFor(stageName: string): readonly string[] {
    const stage = this.stages.find(candidate => candidate.name === stageName)
    if (!stage) throw new Error("Unknown review stage")
    return [...stage.reviewers]
  }
}

function startReview(prototype: ReviewPrototype, draftName: string): ReviewDraft {
  return prototype.clone(draftName)
}

const finance = new ReviewWorkflow("Finance default", [
  { name: "approval", reviewers: ["Hanh"] },
])
const first = startReview(finance, "Q1 draft")
if (first.name !== "Q1 draft" || first.reviewersFor("approval").join(",") !== "Hanh") {
  throw new Error("The draft must inherit configuration and receive its own name")
}

first.addReviewer("approval", "Linh")
const second = startReview(finance, "Q2 draft")
if (first.reviewersFor("approval").join(",") !== "Hanh,Linh" ||
    second.reviewersFor("approval").join(",") !== "Hanh" ||
    finance.reviewersFor("approval").join(",") !== "Hanh") {
  throw new Error("A draft edit must stay in that draft")
}
```

## Khi nên dùng

Dùng Prototype khi một đối tượng đã cấu hình là điểm xuất phát phù hợp nhất cho đối tượng mới, đồng thời quy tắc sao chép thay đổi theo kiểu cụ thể. Xác định trường nào thuộc bản sao, giá trị bất biến nào có thể dùng chung và trường định danh hay vòng đời nào phải tạo lại. Nghiệp vụ quyết định sao chép đến đâu. Bản nháp quy trình có thể kế thừa người rà soát mặc định và nhận tên hoặc ID mới.

## Khi cách đơn giản đã đủ

Factory thông thường nhận một đối tượng tham số sẽ đơn giản hơn nếu đầu vào khởi tạo đã rõ và chỉ có một kiểu cụ thể. Với cấu hình dữ liệu thuần bất biến, dùng chung mẫu và chỉ thay giá trị khác biệt cũng có thể đủ. Dùng phương thức sao chép đa hình khi bên gọi phải tự lặp lại logic khởi tạo hoặc sao chép vốn thuộc về lớp cụ thể.

## Đánh đổi

- Sao chép nông dùng chung trạng thái lồng bên trong và có thể khiến thay đổi ở bản nháp này xuất hiện ở bản khác. Sao chép đồ thị đối tượng lớn làm tăng chi phí CPU và bộ nhớ.
- Các tài nguyên như socket hoặc transaction đang mở có vòng đời riêng. Quyết định khi nào cần kết nối lại hoặc truyền tham chiếu qua ranh giới khác.
- Tiện ích sao chép tổng quát chỉ hỗ trợ những kiểu nhất định. Phương thức clone theo nghiệp vụ có thể giữ hành vi của lớp và chủ động bỏ qua định danh lúc chạy.

## Bài tập

Thêm bước thứ hai rồi tạo hai bản nháp từ cùng mẫu. Bổ sung người rà soát vào bước thứ hai của bản nháp đầu tiên. Kiểm tra bước đầu tiên và cả hai danh sách của bản nháp thứ hai vẫn giữ giá trị ban đầu.

## Tài liệu tham khảo

- [Refactoring.Guru · Prototype](https://refactoring.guru/design-patterns/prototype)

[← Chương trước · 03. Builder](03-builder.md) · [Chương sau → · 05. Singleton](05-singleton.md)
