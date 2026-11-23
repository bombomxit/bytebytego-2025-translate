# 20. State

[Mục lục](../README.md) · [English](../original/20-state.md)

## Bài toán

Một tài liệu đi qua vòng đời thẩm định. Bản nháp có thể gửi thẩm định. Tài liệu đang thẩm định có thể được phê duyệt hoặc trả về để chỉnh sửa. Sau khi phê duyệt, tài liệu đạt trạng thái kết thúc của quy trình này. Sắp tới có thể có thêm trạng thái đã rút, với tập hành động hợp lệ riêng. Nếu mỗi thao tác gửi và phê duyệt tự kiểm tra trạng thái, việc thêm trạng thái có thể buộc sửa mọi handler hiện có.

## Mẫu thiết kế và ranh giới

Cho context giao các quyết định phụ thuộc trạng thái cho state hiện tại. Từng state cụ thể định nghĩa hành vi được phép và có thể chỉ ra state kế tiếp. Context sở hữu state hiện tại và thực hiện chuyển trạng thái đã được cho phép. Hành động không hợp lệ giữ nguyên context và trả kết quả từ chối.

Trong ví dụ, các đối tượng state định nghĩa quy tắc chuyển, còn `DocumentReview` là nơi cập nhật state riêng của nó. Trong ví dụ, trả lại cùng một đối tượng state báo hiệu từ chối. Nếu cho phép thao tác thành công mà giữ nguyên trạng thái, dùng kết quả tường minh để phân biệt việc chấp nhận với việc chuyển trạng thái. Các hành động công khai là yêu cầu có ý nghĩa như `submit`. Bên gọi không trực tiếp gán trạng thái. Với Strategy, bên gọi hoặc cấu hình có thể chọn thuật toán cho một công việc. Với State, vòng đời của đối tượng quyết định hành vi và bước chuyển nào có thể thực hiện khi nhận yêu cầu.

## Ví dụ TypeScript

```typescript
type ReviewAction = "submit" | "approve" | "request-changes";
type Status = "draft" | "in-review" | "approved";

interface ReviewState {
  readonly status: Status;
  next(action: ReviewAction): ReviewState;
}

class DraftState implements ReviewState {
  readonly status = "draft";

  next(action: ReviewAction): ReviewState {
    return action === "submit" ? new InReviewState() : this;
  }
}

class InReviewState implements ReviewState {
  readonly status = "in-review";

  next(action: ReviewAction): ReviewState {
    if (action === "approve") return new ApprovedState();
    if (action === "request-changes") return new DraftState();
    return this;
  }
}

class ApprovedState implements ReviewState {
  readonly status = "approved";

  next(_action: ReviewAction): ReviewState {
    return this;
  }
}

class DocumentReview {
  private state: ReviewState = new DraftState();

  status(): Status {
    return this.state.status;
  }

  dispatch(action: ReviewAction): boolean {
    const next = this.state.next(action);
    if (next === this.state) return false;
    this.state = next;
    return true;
  }
}

const review = new DocumentReview();
if (review.dispatch("approve") || review.status() !== "draft") {
  throw new Error("A draft cannot be approved directly");
}
if (!review.dispatch("submit") || review.status() !== "in-review") {
  throw new Error("Submitting a draft should move it into review");
}
if (!review.dispatch("request-changes") || review.status() !== "draft") {
  throw new Error("A request for changes should return the document to draft");
}
if (!review.dispatch("submit") || !review.dispatch("approve")) {
  throw new Error("A revised draft should be eligible for approval");
}
if (review.dispatch("request-changes") || review.status() !== "approved") {
  throw new Error("An approved review is terminal in this workflow");
}
```

## Khi nên dùng

Dùng State khi cùng một thao tác có hành vi khác nhau theo giai đoạn của vòng đời và mỗi giai đoạn đang có thêm quy tắc riêng. Nếu các tác nhân trong quy trình có quyền khác nhau, kiểm tra quyền trước khi áp dụng bước chuyển.

### Bài toán thường gặp

- **Phê duyệt hồ sơ.** Bản nháp có thể gửi, hồ sơ đang duyệt có thể được phê duyệt hoặc trả về, còn hồ sơ đã phê duyệt có quy tắc riêng. Gom cách xử lý từng hành động theo trạng thái. Với dữ liệu lưu trong cơ sở dữ liệu, kiểm tra phiên bản khi ghi để hai thao tác đồng thời không cùng đi tiếp từ một trạng thái cũ.
- **Xử lý vòng đời một lượt nhập dữ liệu.** Thao tác hủy có thể bỏ ngay lượt đang chờ và gửi yêu cầu dừng cho lượt đang chạy. Lượt đã hoàn tất có thể từ chối thao tác này. Bảng chuyển trạng thái thường đủ khi mỗi bước chỉ xác định trạng thái kế tiếp và chưa có hành vi riêng.

## Khi cách đơn giản đã đủ

Nếu đồ thị chuyển trạng thái nhỏ và chưa có hành vi riêng theo state, lập một bảng hành động và kết quả hợp lệ để dễ thấy toàn bộ đồ thị. Một lệnh switch ngắn cũng có thể phục vụ quy trình hai trạng thái ổn định.

## Đánh đổi

Hành vi được gom theo state, còn người đọc có thể phải xem nhiều lớp mới thấy toàn bộ đồ thị. Kiểm thử mọi bước chuyển hợp lệ, các hành động bị từ chối và các trạng thái kết thúc. Quy trình có lưu trạng thái cần cập nhật nguyên tử hoặc kiểm tra phiên bản để hai yêu cầu đồng thời không cùng được chấp nhận dựa trên một trạng thái cũ.

## Bài tập

Thêm trạng thái đã rút khi gửi `withdraw` cho tài liệu đang thẩm định. Kiểm tra thao tác rút bị từ chối ở trạng thái nháp, thực hiện được trong lúc thẩm định và khiến tài liệu sau đó không thể được phê duyệt.

## Tài liệu tham khảo

- [State · Refactoring.Guru](https://refactoring.guru/design-patterns/state)

[← Chương trước · 19. Observer](19-observer.md) · [Chương sau → · 21. Strategy](21-strategy.md)
