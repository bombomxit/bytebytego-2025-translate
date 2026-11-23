# 15. Interpreter

[Mục lục](../README.md) · [English](../original/15-interpreter.md)

## Bài toán

Quản trị viên cấu hình cách cổng tài liệu chọn hồ sơ cần thẩm định. Một nhóm yêu cầu tài liệu vừa có nhãn đối ngoại vừa đạt số trang tối thiểu. Nhóm khác kết hợp những điều kiện đó theo cách khác. Cổng cần một tập phép kiểm tra có thể ghép thành quy tắc và áp dụng lặp lại cho nhiều hồ sơ.

## Mẫu thiết kế và ranh giới

Định nghĩa một ngữ pháp nhỏ và gắn hành vi đánh giá vào các nút biểu thức của nó. Các điều kiện kiểm tra nhãn và số trang trong ví dụ là biểu thức đầu cuối. `And` là biểu thức không đầu cuối, giao việc đánh giá cho hai biểu thức con và có hành vi đoản mạch như toán tử `&&`. Thông tin về tài liệu là ngữ cảnh truyền cho cả cây biểu thức. Các nút lá đọc thông tin đó, còn các toán tử kết hợp kết quả.

Ví dụ dựng trực tiếp cây biểu thức. Nếu quy tắc viết dưới dạng văn bản, parser phải chuyển văn bản thành cây và báo lỗi cú pháp. Việc đánh giá bắt đầu sau khi đã có cây hợp lệ. Tách rõ các bước giúp dùng chung bộ đánh giá cho cả giao diện tạo quy tắc bằng biểu mẫu lẫn định dạng văn bản.

## Ví dụ TypeScript

```typescript
type DocumentFacts = Readonly<{ labels: readonly string[]; pages: number }>;

interface Expression {
  evaluate(facts: DocumentFacts): boolean;
}

class HasLabel implements Expression {
  constructor(private readonly label: string) {}

  evaluate(facts: DocumentFacts): boolean {
    return facts.labels.includes(this.label);
  }
}

class AtLeastPages implements Expression {
  constructor(private readonly threshold: number) {}

  evaluate(facts: DocumentFacts): boolean {
    return facts.pages >= this.threshold;
  }
}

class And implements Expression {
  constructor(
    private readonly left: Expression,
    private readonly right: Expression,
  ) {}

  evaluate(facts: DocumentFacts): boolean {
    return this.left.evaluate(facts) && this.right.evaluate(facts);
  }
}

const needsReview = new And(new HasLabel("external"), new AtLeastPages(10));
if (!needsReview.evaluate({ labels: ["external"], pages: 10 })) {
  throw new Error("A matching label and the inclusive threshold must pass");
}
if (needsReview.evaluate({ labels: ["external"], pages: 9 })) {
  throw new Error("The label alone is insufficient");
}
if (needsReview.evaluate({ labels: ["internal"], pages: 18 })) {
  throw new Error("The page count alone is insufficient");
}
```

## Khi nên dùng

Dùng khi các phép toán cho phép tạo thành một tập nhỏ, ổn định, các quy tắc có thể tổ hợp, và ứng dụng cần đánh giá nhiều biểu thức theo cùng cách diễn giải.

### Bài toán thường gặp

- **Ghép bộ lọc hồ sơ.** Chọn các phép có sẵn như kiểm tra nhãn, so sánh số trang, và ghép điều kiện bằng phép VÀ hoặc HOẶC. Mỗi nút của cây biết cách tính kết quả từ dữ liệu hồ sơ. Nếu cho nhập dưới dạng văn bản, bước phân tích cú pháp dựng cây trước khi đánh giá.
- **Cấu hình điều kiện chuyển xử lý.** Người quản trị ghép điều kiện theo nhóm hồ sơ và thuộc tính đã công bố. Giới hạn tập phép toán, kiểu tham số và độ sâu biểu thức, để người dùng có thể dự đoán kết quả. Nếu nghiệp vụ chỉ có vài quy tắc cố định, dùng biểu thức thông thường trong mã.

## Khi cách đơn giản đã đủ

Một quy tắc cố định thường dễ đọc dưới dạng biểu thức Boolean trực tiếp. Nếu ứng dụng đã dùng ngôn ngữ truy vấn trưởng thành cho đúng mục đích đó, hãy dùng các điều kiện và cơ chế kiểm tra hợp lệ mà nó hỗ trợ.

## Đánh đổi

Mỗi cấu trúc mới đều bổ sung ngữ nghĩa cần giải thích và kiểm thử, kể cả khi kết hợp với các toán tử đang có. Với quy tắc do người dùng nhập, kiểm tra các toán tử và đối số được chấp nhận, đồng thời giới hạn kích thước và độ sâu của quy tắc. Ngữ pháp lớn hoặc tần suất xử lý cao có thể cần parser, compiler hay rules engine chuyên dụng.

## Bài tập

Thêm biểu thức `Or` nhận cùng hai biểu thức con. Kiểm tra tài liệu đối ngoại có chín trang và tài liệu nội bộ có mười trang đều đạt, còn tài liệu nội bộ có chín trang không đạt.

## Tài liệu tham khảo

- [Interpreter · Design Patterns, Gang of Four](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-9780201633610)

[← Chương trước · 14. Command](14-command.md) · [Chương sau → · 16. Iterator](16-iterator.md)
