# 18. Memento

[Mục lục](../README.md) · [English](../original/18-memento.md)

## Bài toán

Trình soạn thảo cho người dùng lưu các điểm khôi phục khi sửa tài liệu. Tài liệu hiện có tiêu đề và các thẻ. Sau này nó có thể thêm trường riêng như ghi chú thẩm định hay chế độ chỉnh sửa. Thành phần giữ điểm khôi phục cần phục hồi toàn bộ bản nháp mà không cần biết cách lưu từng trường mới.

## Mẫu thiết kế và ranh giới

Originator tự ghi nhận trạng thái của mình và tạo memento. Caretaker giữ memento và yêu cầu originator khôi phục khi cần. Caretaker chỉ cần biết sẽ dùng điểm nào. Originator chịu trách nhiệm về định dạng snapshot và cách áp dụng nó.

Trong ví dụ, `Draft` là originator. Biến giữ `checkpoint` đại diện cho trình quản lý lịch sử hoặc điểm khôi phục. Memento là một token không lộ dữ liệu trạng thái, với dữ liệu tương ứng nằm trong `WeakMap` riêng của từng bản nháp. Bản nháp khác không dùng được token đó. Mảng thẻ được sao chép để thay đổi dữ liệu mà bên gọi truyền vào không làm đổi ngầm điểm khôi phục. Các giá trị bên trong mảng là chuỗi bất biến.

## Ví dụ TypeScript

```typescript
type DraftMemento = object;

class Draft {
  private title: string;
  private tags: string[];
  private readonly snapshots = new WeakMap<
    DraftMemento,
    Readonly<{ title: string; tags: readonly string[] }>
  >();

  constructor(title: string, tags: readonly string[]) {
    this.title = title;
    this.tags = [...tags];
  }

  revise(title: string, tags: readonly string[]): void {
    this.title = title;
    this.tags = [...tags];
  }

  view(): Readonly<{ title: string; tags: readonly string[] }> {
    return { title: this.title, tags: [...this.tags] };
  }

  save(): DraftMemento {
    const memento = Object.freeze({});
    this.snapshots.set(memento, this.view());
    return memento;
  }

  restore(memento: DraftMemento): boolean {
    const snapshot = this.snapshots.get(memento);
    if (!snapshot) return false;
    this.revise(snapshot.title, snapshot.tags);
    return true;
  }
}

const draft = new Draft("Agenda", ["planning"]);
const checkpoint = draft.save();
draft.revise("Published agenda", ["public"]);

if (!draft.restore(checkpoint)) {
  throw new Error("The draft must accept its own checkpoint");
}
const restored = draft.view();
if (restored.title !== "Agenda" || restored.tags.join() !== "planning") {
  throw new Error("Restore must recover both the title and the tag collection");
}

const otherDraft = new Draft("Notes", []);
if (otherDraft.restore(checkpoint) || otherDraft.view().title !== "Notes") {
  throw new Error("A checkpoint must only restore its owner");
}
```

## Khi nên dùng

Dùng Memento khi cần khôi phục một trạng thái nội bộ nhất quán và nhiều trường có thể đổi cùng nhau. Điểm khôi phục phù hợp với các chỉnh sửa có thể quay lại theo snapshot, kể cả khi từng chỉnh sửa không có thao tác nghịch đảo riêng.

## Khi cách đơn giản đã đủ

Nếu chỉ cần khôi phục một giá trị vô hướng, giữ giá trị trước đó ngay tại nơi sở hữu nó. Một giá trị bất biến cũng có thể làm snapshot nếu cấu trúc đầy đủ của nó phù hợp để công khai.

## Đánh đổi

Snapshot đầy đủ tốn bộ nhớ theo lượng dữ liệu giữ lại. Giới hạn độ dài lịch sử hoặc dùng cách biểu diễn chia sẻ dữ liệu bất biến nếu dung lượng checkpoint tăng đáng kể. Ví dụ giữ checkpoint trong bộ nhớ và gắn nó với một bản nháp. Nếu cần lưu bền vững, phải có định dạng ổn định, quy tắc nâng cấp định dạng và chính sách truy cập kho lưu trữ phù hợp với dữ liệu.

## Bài tập

Thêm trường ngôn ngữ cho bản nháp, rồi lưu checkpoint trước khi đổi cả ngôn ngữ và tiêu đề. Kiểm tra restore khôi phục cả hai trong khi mã giữ checkpoint vẫn giữ nguyên.

## Tài liệu tham khảo

- [Memento · Refactoring.Guru](https://refactoring.guru/design-patterns/memento)

[← Chương trước · 17. Mediator](17-mediator.md) · [Chương sau → · 19. Observer](19-observer.md)
