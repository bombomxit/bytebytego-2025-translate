# 11. Flyweight

[Mục lục](../README.md) · [English](../original/11-flyweight.md)

## Bài toán

Một canvas quy trình hiển thị hàng nghìn nút. Nhiều nút dùng cùng hình dạng và màu viền vì hai thuộc tính này phụ thuộc loại nút và theme. Mỗi nút vẫn có mã và tọa độ riêng. Nếu số liệu profiling cho thấy các đối tượng style trùng lặp làm heap tăng, dùng một đối tượng style chuẩn cho mỗi cặp loại nút và theme có thể giảm số lần cấp phát. Với style chứa nhiều thuộc tính hơn, lợi ích có thể thấy rõ ngay cả khi canvas chỉ có vài loại nút.

## Mẫu thiết kế và ranh giới

Flyweight chia sẻ trạng thái nội tại lặp lại và để trạng thái ngoại tại ở từng đối tượng sử dụng hoặc bên gọi. Trong ví dụ, `NodeStyle` đã được đóng băng là phần nội tại. Mã và tọa độ thuộc phần ngoại tại, nằm trên `DiagramNode`. `StylePool` vừa tạo vừa lưu đối tượng chuẩn theo khóa. Khóa phải chứa mọi đầu vào làm đổi các trường dùng chung. Trạng thái riêng của từng nút, chẳng hạn nút nào đang được chọn, có thể thay đổi độc lập và nằm ngoài khóa.

## Ví dụ TypeScript

Hai nút cùng loại và theme dùng chung một đối tượng style nhưng giữ tọa độ riêng. Các kiểm tra còn cho thấy theme khác tạo style khác, và loại nút khác có thể đổi hình dạng.

```typescript
type NodeKind = "task" | "approval";
type Theme = "light" | "dark";
type NodeStyle = Readonly<{ shape: "box" | "diamond"; border: string }>;

class StylePool {
  private readonly styles = new Map<string, NodeStyle>();

  get(kind: NodeKind, theme: Theme): NodeStyle {
    const key = kind + "/" + theme;
    const existing = this.styles.get(key);
    if (existing !== undefined) return existing;

    const style: NodeStyle = Object.freeze({
      shape: kind === "task" ? "box" : "diamond",
      border: theme === "light" ? "#202020" : "#e0e0e0",
    });
    this.styles.set(key, style);
    return style;
  }
}

type DiagramNode = { id: string; x: number; y: number; style: NodeStyle };
const styles = new StylePool();

function approvalNode(id: string, x: number, theme: Theme): DiagramNode {
  return { id, x, y: 12, style: styles.get("approval", theme) };
}

const first = approvalNode("n1", 10, "light");
const second = approvalNode("n2", 40, "light");
const dark = approvalNode("n3", 75, "dark");

if (first.x === second.x || first.style !== second.style ||
    !Object.isFrozen(first.style)) {
  throw new Error("Each node should keep its position and share an immutable style");
}
const taskStyle = styles.get("task", "light");
if (dark.style === first.style || dark.style.border === first.style.border ||
    taskStyle === first.style || first.style.shape !== "diamond" || taskStyle.shape !== "box") {
  throw new Error("The style key should preserve theme and node kind");
}
```

## Khi nên dùng

Dùng khi nhiều đối tượng đang tồn tại lặp lại trạng thái ổn định và phép đo cho thấy chia sẻ giúp giảm bộ nhớ hoặc chi phí khởi tạo. Ví dụ chỉ có bốn khóa khả dĩ. Nếu style đến từ cấu hình, hãy chọn phạm vi pool phù hợp với vòng đời của dữ liệu cần chia sẻ.

### Bài toán thường gặp

- **Lưu kiểu trình bày của sơ đồ lớn.** Nút cùng loại và chủ đề chia sẻ thông tin hình dạng, màu viền và phông chữ. Tọa độ và trạng thái chọn vẫn thuộc từng nút. Thông tin dùng chung cần bất biến, đồng thời khóa tra cứu phải bao gồm mọi yếu tố làm thay đổi kiểu trình bày.
- **Dùng chung phông và biểu tượng trong trình kết xuất.** Nhiều phần tử có thể tham chiếu cùng mô tả biểu tượng và giữ vị trí riêng. Đo bộ nhớ trước khi tạo kho đối tượng dùng chung. Nếu số biến thể tăng theo dữ liệu đầu vào, đặt phạm vi theo tài liệu hoặc giới hạn lượng mô tả giữ lại.

## Khi cách đơn giản đã đủ

Dùng hằng số hoặc map tĩnh với vài tổ hợp đã biết. Có thể lưu giá trị vô hướng hoặc mã style nếu bên đọc đã có cách tra cứu hiệu quả. Giữ biểu diễn riêng trên từng nút đến khi áp lực cấp phát đủ lớn để cần pool.

## Đánh đổi

Tra cứu pool phát sinh thêm một ít công việc. Pool giữ các khóa duy nhất vô thời hạn có thể tốn nhiều bộ nhớ hơn lượng tiết kiệm được. Khi khóa thay đổi động, giới hạn pool theo canvas hoặc đặt chính sách lưu giữ. Trạng thái chia sẻ phải bất biến trên thực tế. `Object.freeze` chỉ đóng băng lớp ngoài, nên đối tượng style trong ví dụ chỉ có các giá trị nguyên thủy.

## Bài tập

Thêm viền đánh dấu cho nút đang được chọn. Vẽ viền từ trạng thái riêng của nút đó và kiểm tra rằng việc đổi lựa chọn không làm thay đổi style dùng chung hay các nút khác.

## Tài liệu tham khảo

- [Flyweight — Refactoring.Guru](https://refactoring.guru/design-patterns/flyweight)

[← Chương trước · 10. Facade](10-facade.md) · [Chương sau → · 12. Proxy](12-proxy.md)
