# 17. Mediator

[Mục lục](../README.md) · [English](../original/17-mediator.md)

## Bài toán

Hộp thoại tải lên có bộ chọn tệp, ô xác nhận đồng ý và nút gửi. Nút gửi chỉ bật khi người dùng đã chọn tệp và đồng ý. Nếu mỗi trường tự cập nhật nút gửi, mỗi bên phải biết cả trường còn lại. Một hộp thoại khác có thể dùng lại các thành phần này và yêu cầu thêm trường phân loại tài liệu.

## Mẫu thiết kế và ranh giới

Cho các thành phần báo thay đổi về một mediator. Mediator chịu trách nhiệm về quy tắc phối hợp và cập nhật những thành phần liên quan. Trong mẫu này, các thành phần là colleague. Mỗi bên phát sự kiện riêng mà không cần biết thành phần nào khác sẽ phản hồi.

Bộ chọn tệp và ô xác nhận gửi sự kiện qua `UploadFormEvents`. `UploadFormMediator` kết hợp dữ liệu đầu vào và cập nhật `SubmitButton`. Mediator này có phạm vi một biểu mẫu. Trong framework giao diện, có thể render nút dựa trên trạng thái suy ra từ biểu mẫu. Hướng phối hợp vẫn giữ nguyên khi biểu mẫu sở hữu quy tắc và các trường báo thay đổi về nó.

## Ví dụ TypeScript

```typescript
interface UploadFormEvents {
  fileSelected(name: string | null): void;
  consentChanged(accepted: boolean): void;
}

class FilePicker {
  constructor(private readonly events: UploadFormEvents) {}

  select(name: string | null): void {
    this.events.fileSelected(name);
  }
}

class ConsentCheckbox {
  constructor(private readonly events: UploadFormEvents) {}

  toggle(accepted: boolean): void {
    this.events.consentChanged(accepted);
  }
}

class SubmitButton {
  enabled = false;
}

class UploadFormMediator implements UploadFormEvents {
  readonly picker = new FilePicker(this);
  readonly consent = new ConsentCheckbox(this);
  readonly submit = new SubmitButton();

  private selectedFile: string | null = null;
  private hasConsent = false;

  fileSelected(name: string | null): void {
    this.selectedFile = name;
    this.updateSubmit();
  }

  consentChanged(accepted: boolean): void {
    this.hasConsent = accepted;
    this.updateSubmit();
  }

  private updateSubmit(): void {
    this.submit.enabled = this.selectedFile !== null && this.hasConsent;
  }
}

const form = new UploadFormMediator();
form.consent.toggle(true);
if (form.submit.enabled) {
  throw new Error("Consent alone must leave the button disabled");
}
form.picker.select("proposal.pdf");
if (!form.submit.enabled) {
  throw new Error("A selected file and consent must enable the button");
}
form.picker.select(null);
if (form.submit.enabled) {
  throw new Error("Removing the file must disable the button again");
}
```

## Khi nên dùng

Dùng khi nhiều thành phần có thể tái sử dụng cần phối hợp và việc thay đổi một thành phần đang làm lan thêm phụ thuộc sang các thành phần khác. Giới hạn mỗi mediator ở một tương tác thống nhất như một biểu mẫu hay một bước quy trình.

### Bài toán thường gặp

- **Phối hợp các trường trên biểu mẫu.** Bộ chọn tệp, ô đồng ý và trường phân loại báo thay đổi cho bộ điều phối của biểu mẫu. Bộ điều phối tính khi nào được bật nút gửi, giúp từng trường không cần biết các trường còn lại. Máy chủ vẫn kiểm tra dữ liệu khi nhận yêu cầu.
- **Đồng bộ thao tác trong trình soạn thảo.** Khi người dùng chọn một đoạn, thanh công cụ và bảng thuộc tính đều cần cập nhật. Bộ điều phối nhận thao tác chọn và phân phối phần cập nhật cần thiết. Giới hạn phạm vi theo mỗi cửa sổ soạn thảo để một lựa chọn không làm đổi cửa sổ khác.

## Khi cách đơn giản đã đủ

Nếu thành phần biểu mẫu đã nhận các giá trị đầu vào và tính được một cờ vô hiệu hóa, dùng luôn thành phần đó với một biểu thức đơn giản. Ranh giới trách nhiệm quan trọng hơn việc thêm lớp.

## Đánh đổi

Quy tắc phối hợp dễ tìm hơn, nhưng mediator có thể tích tụ các quy tắc không liên quan và biết quá nhiều về các thành phần. Giữ quy tắc nghiệp vụ trong model phụ trách và tập trung mediator vào tương tác. Điều kiện bật nút hỗ trợ giao diện. Máy chủ vẫn chịu trách nhiệm kiểm tra yêu cầu gửi lên.

## Bài tập

Thêm trường phân loại có sự kiện gửi về mediator. Kiểm tra rằng chọn tệp và đồng ý vẫn chưa bật nút, còn chọn thêm phân loại sẽ bật nút mà không cần sửa hai trường cũ.

## Tài liệu tham khảo

- [Mediator · Refactoring.Guru](https://refactoring.guru/design-patterns/mediator)

[← Chương trước · 16. Iterator](16-iterator.md) · [Chương sau → · 18. Memento](18-memento.md)
