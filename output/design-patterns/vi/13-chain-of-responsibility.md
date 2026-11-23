# 13. Chain of Responsibility

[Mục lục](../README.md) · [English](../original/13-chain-of-responsibility.md)

## Bài toán

Một cổng tài liệu chuyển hồ sơ đến hàng đợi thẩm định. Hồ sơ nhiều trang được chuyển đến chuyên viên cấp cao, còn hồ sơ thuộc diện tuân thủ được chuyển đến người phụ trách chuyên môn. Một hồ sơ có thể thỏa cả hai điều kiện, với quy tắc tuân thủ được ưu tiên. Khách hàng tiếp theo có thể yêu cầu thêm quy tắc thẩm định pháp lý ở giữa hai quy tắc đó.

Cổng tài liệu đã biết cách đưa hồ sơ vào hàng đợi. Phần hay thay đổi là danh sách và thứ tự các quy tắc chọn hàng đợi.

## Mẫu thiết kế và ranh giới

Mỗi handler nhận cùng một kiểu yêu cầu và có cách báo rằng nó từ chối xử lý. Chuỗi dừng ở handler đầu tiên nhận trách nhiệm. Bên gọi giao yêu cầu cho cả chuỗi, còn nơi lắp ghép chuỗi quyết định thứ tự ưu tiên.

Ví dụ dùng các hàm làm handler. Bộ điều phối duyệt một mảng có thứ tự, tương đương việc chuyển tiếp qua tham chiếu đến handler kế trong một chuỗi liên kết. Mã hàng đợi được trả về cổng tài liệu để cổng thực hiện bước tiếp theo. Nếu duyệt hết chuỗi vẫn chưa có handler nhận, hàm trả `undefined` để cổng áp dụng chính sách riêng cho hồ sơ chưa được phân công.

## Ví dụ TypeScript

```typescript
type ReviewRequest = Readonly<{ pages: number; regulated: boolean }>;
type Queue = "compliance" | "senior-review";
type ReviewHandler = (request: ReviewRequest) => Queue | undefined;

const compliance: ReviewHandler = request =>
  request.regulated ? "compliance" : undefined;
const seniorReview: ReviewHandler = request =>
  request.pages > 50 ? "senior-review" : undefined;

function selectQueue(
  request: ReviewRequest,
  handlers: readonly ReviewHandler[],
): Queue | undefined {
  for (const handle of handlers) {
    const queue = handle(request);
    if (queue !== undefined) return queue;
  }
  return undefined;
}

const handlers = [compliance, seniorReview];
if (selectQueue({ regulated: false, pages: 70 }, handlers) !== "senior-review") {
  throw new Error("A declining handler must pass the request onward");
}
if (selectQueue({ regulated: true, pages: 70 }, handlers) !== "compliance") {
  throw new Error("Compliance must take precedence when both rules match");
}
if (selectQueue({ regulated: false, pages: 5 }, handlers) !== undefined) {
  throw new Error("An unmatched request must remain unassigned");
}
```

## Khi nên dùng

Dùng khi điều kiện giữa các quy tắc có thể chồng lấn, thứ tự ảnh hưởng đến kết quả, và từng đợt triển khai có thể thêm hoặc sắp xếp lại các quy tắc do nhiều bên phụ trách. Nếu bên gọi cần retry an toàn, giữ bước chọn hàng đợi không thực hiện thao tác ghi.

## Khi cách đơn giản đã đủ

Hai phép kiểm tra ổn định có thể đặt trong một hàm. Nếu luôn quyết định được bằng một khóa chính xác như loại tài liệu khai báo, dùng bảng tra cứu.

## Đánh đổi

Vị trí của quy tắc trở thành một phần của hành vi. Một quy tắc rộng đặt sớm có thể che mất quy tắc chuyên biệt phía sau, nên cần kiểm thử cả các yêu cầu thỏa nhiều điều kiện lẫn từng quy tắc riêng. Quy định rõ ngoại lệ sẽ dừng việc chuyển tiếp hay được ánh xạ thành một kết quả đã biết.

## Bài tập

Thêm handler thẩm định pháp lý dựa trên một cờ mới trong yêu cầu. Hồ sơ thuộc diện tuân thủ và có cờ đó vẫn phải vào hàng đợi tuân thủ. Hồ sơ chỉ có cờ mới phải vào hàng đợi pháp lý, còn hồ sơ không khớp phải giữ trạng thái chưa phân công.

## Tài liệu tham khảo

- [Chain of Responsibility · Refactoring.Guru](https://refactoring.guru/design-patterns/chain-of-responsibility)

[← Chương trước · 12. Proxy](12-proxy.md) · [Chương sau → · 14. Command](14-command.md)
