# 14. Command

[Mục lục](../README.md) · [English](../original/14-command.md)

## Bài toán

Trình soạn thảo cho phép sửa bản nháp qua thanh công cụ, phím tắt và menu. Nó cần một thao tác Undo chung để hoàn tác chỉnh sửa gần nhất, bất kể thao tác đó bắt đầu từ đâu. Kiểu chỉnh sửa tiếp theo có thể là bật cờ cho một mục hoặc di chuyển đoạn văn. Nút Undo cần hoạt động khi có thêm các kiểu chỉnh sửa đó.

## Mẫu thiết kế và ranh giới

Biểu diễn một yêu cầu bằng đối tượng có giao diện thực thi. Bên phát lệnh tạo command kèm đối tượng đích và các tham số. Invoker thực thi command và áp dụng chính sách chung, chẳng hạn ghi lại các chỉnh sửa đã hoàn tất. Receiver là bản nháp nhận thay đổi.

Trong ví dụ, `RenameDraft` ghi nhận tiêu đề trước đó ngay lúc thực thi. Thời điểm này quan trọng vì bản nháp có thể đổi từ lúc tạo command đến lúc chạy nó. `EditHistory` phụ thuộc vào `EditCommand` và hoàn tác theo thứ tự ngược với lúc thực thi. Mỗi chỉnh sửa trong ví dụ dùng một command mới. Ví dụ giả định một trình soạn thảo sở hữu lịch sử và thực hiện các chỉnh sửa tuần tự.

## Ví dụ TypeScript

```typescript
interface EditCommand {
  execute(): void;
  undo(): void;
}

class Draft {
  constructor(private title: string) {}

  getTitle(): string {
    return this.title;
  }

  rename(title: string): void {
    this.title = title;
  }
}

class RenameDraft implements EditCommand {
  private previousTitle: string | undefined;

  constructor(private readonly draft: Draft, private readonly title: string) {}

  execute(): void {
    this.previousTitle = this.draft.getTitle();
    this.draft.rename(this.title);
  }

  undo(): void {
    if (this.previousTitle === undefined) {
      throw new Error("Rename must run before it can be undone");
    }
    this.draft.rename(this.previousTitle);
    this.previousTitle = undefined;
  }
}

class EditHistory {
  private readonly completed: EditCommand[] = [];

  run(command: EditCommand): void {
    command.execute();
    this.completed.push(command);
  }

  undoLast(): boolean {
    const command = this.completed.at(-1);
    if (!command) return false;
    command.undo();
    this.completed.pop();
    return true;
  }
}

const draft = new Draft("Draft");
const commandHistory = new EditHistory();
commandHistory.run(new RenameDraft(draft, "Proposal"));
commandHistory.run(new RenameDraft(draft, "Signed proposal"));
if (draft.getTitle() !== "Signed proposal") {
  throw new Error("The last rename should be visible");
}
if (!commandHistory.undoLast() || draft.getTitle() !== "Proposal") {
  throw new Error("Undo should restore the title immediately before the last edit");
}
if (!commandHistory.undoLast() || draft.getTitle() !== "Draft" || commandHistory.undoLast()) {
  throw new Error("Undo must follow reverse execution order and stop on empty history");
}
```

## Khi nên dùng

Dùng khi các thao tác chia sẻ chính sách thực thi như hoàn tác, lên lịch hoặc ghi nhận, trong khi từng thao tác vẫn phát triển độc lập. Với hệ thống chạy job bền vững, hãy lưu mô tả yêu cầu có phiên bản rồi tìm handler khi xử lý.

## Khi cách đơn giản đã đủ

Nếu một nút chỉ gọi ngay một thao tác và ứng dụng chưa có chính sách thực thi dùng chung, gọi hàm trực tiếp giúp luồng dễ đọc.

## Đánh đổi

Mỗi thao tác cần định nghĩa cách thực thi và cách đảo ngược tác động nếu có hỗ trợ hoàn tác. Undo chỉ khả thi khi thông tin đã lưu và trạng thái receiver còn phù hợp. Ví dụ, email đã gửi có thể cần một hành động bù trừ riêng. Retry command đã lưu cũng cần chính sách xử lý giao trùng và lỗi sau khi đã thực hiện một phần công việc.

## Bài tập

Thêm thao tác bật hoặc tắt cờ lưu trữ của bản nháp. Chạy lệnh đổi tên rồi lệnh đổi cờ qua cùng lịch sử. Lần Undo đầu phải khôi phục cờ và giữ tiêu đề mới, lần thứ hai phải khôi phục tiêu đề ban đầu.

## Tài liệu tham khảo

- [Command · Refactoring.Guru](https://refactoring.guru/design-patterns/command)

[← Chương trước · 13. Chain of Responsibility](13-chain-of-responsibility.md) · [Chương sau → · 15. Interpreter](15-interpreter.md)
