# 05. Singleton

[Mục lục](../README.md) · [English](../original/05-singleton.md)

## Bài toán

Ứng dụng tiếp nhận tài liệu trên máy tính điều khiển một máy quét vật lý. Màn hình nhập và tác vụ nền cùng chạy trong một phiên bản ứng dụng, nên cần phối hợp khi truy cập thiết bị. Nếu mỗi bên tự tạo bộ điều phối trong bộ nhớ, cả hai có thể thấy máy quét đang rảnh và cùng bắt đầu quét. Nhu cầu duy nhất ở đây xuất phát từ việc có một tài nguyên và một đầu mối quản lý đã thống nhất.

## Mẫu thiết kế và ranh giới

`ScannerGate` giới hạn cách tạo instance thông qua constructor private và cung cấp một instance dùng chung qua `getInstance()`. Instance giữ cờ bận và cấp hàm nhả quyền cho bên đang giữ quyền. Nó điều phối những bên gọi cùng lớp trong một instance module đã nạp. Tab trình duyệt, worker, tiến trình riêng và bản module khác nhau có thể giữ instance riêng.

## Ví dụ TypeScript

Ví dụ giả định một ngữ cảnh thực thi JavaScript. `tryAcquire()` cập nhật cờ đồng bộ nên lần gọi thứ hai trong cùng ngữ cảnh thấy ngay tài nguyên đã được giữ. Gọi lại hàm nhả quyền cũ không thể nhả quyền của lượt đến sau. Trong mã quét thực tế, bên gọi nhả quyền ở khối `finally` sau khi thao tác kết thúc.

```typescript
class ScannerGate {
  static readonly #instance = new ScannerGate()
  #occupied = false

  private constructor() {}

  static getInstance(): ScannerGate {
    return ScannerGate.#instance
  }

  tryAcquire(): (() => void) | undefined {
    if (this.#occupied) return undefined
    this.#occupied = true

    let released = false
    return () => {
      if (released) return
      released = true
      this.#occupied = false
    }
  }
}

const importScreen = ScannerGate.getInstance()
const backgroundJob = ScannerGate.getInstance()
const releaseImport = importScreen.tryAcquire()
if (!releaseImport || importScreen !== backgroundJob ||
    backgroundJob.tryAcquire() !== undefined) {
  throw new Error("Both entry points must coordinate through the same gate")
}

releaseImport()
const releaseBackground = backgroundJob.tryAcquire()
if (!releaseBackground) throw new Error("Releasing must let the next caller acquire")

releaseImport()
if (importScreen.tryAcquire() !== undefined) {
  throw new Error("An old release function must not unlock a later claim")
}
releaseBackground()
```

## Khi nên dùng

Cân nhắc Singleton khi việc chỉ có một đầu mối là ràng buộc chủ đích trong một phạm vi quản lý rõ ràng và nhiều đường vào cần tìm cùng đối tượng đó. Ghi rõ tiến trình hoặc container nào tạo nó, khi nào khởi tạo và bên nào chịu trách nhiệm dọn dẹp khi tắt nếu đối tượng quản lý tài nguyên.

### Bài toán thường gặp

- **Điều phối tác vụ trong một tiến trình.** Nhiều điểm vào cùng nộp việc cho một bộ điều phối để áp dụng chung giới hạn số việc chạy đồng thời. Phạm vi duy nhất là tiến trình đó. Nếu nhiều tiến trình cần cùng tuân theo một giới hạn, phải có cơ chế điều phối dùng chung.
- **Quản lý một tài nguyên độc quyền.** Nếu một tiến trình chỉ được mở một phiên giao tiếp với thiết bị, một đối tượng quản lý có thể nắm quyền mở, cấp quyền sử dụng và đóng phiên khi tắt. Nếu ứng dụng có một điểm khởi tạo rõ ràng, tạo rồi truyền đối tượng đó vào nơi cần dùng thường đủ.

## Khi cách đơn giản đã đủ

Nếu kiểm soát được lúc khởi động ứng dụng, hãy tạo một đối tượng ở đó rồi inject cùng instance vào màn hình nhập và tác vụ nền. Cách này làm rõ dependency và vòng đời. Tiện ích không giữ trạng thái có thể là hàm module. Nếu nhiều tiến trình độc lập cần dùng chung máy quét, hãy phối hợp thông qua driver thiết bị hoặc một đầu mối mà tất cả tiến trình đều truy cập được.

## Đánh đổi

- Phương thức truy cập static che khuất dependency tại nơi gọi và trạng thái dùng chung có thể tồn tại qua nhiều test trong cùng runtime.
- Chỉ định một đầu mối giúp điều phối dễ hơn. Dùng đối tượng có trạng thái chung làm dịch vụ toàn cục có thể tạo phụ thuộc ngoài ý muốn giữa các tính năng.
- Bộ điều phối trong bộ nhớ chỉ có tác dụng trong phạm vi runtime đã nêu. Nó không thể bảo đảm truy cập độc quyền thiết bị nếu mã ở nơi khác truy cập vòng qua đầu mối.

## Bài tập

Viết hàm `scan()` lấy quyền sử dụng máy quét và nhả quyền trong `finally`. Cho lần quét đầu ném lỗi rồi kiểm tra lần sau vẫn lấy được quyền.

## Tài liệu tham khảo

- [Refactoring.Guru · Singleton](https://refactoring.guru/design-patterns/singleton)

[← Chương trước · 04. Prototype](04-prototype.md) · [Chương sau → · 06. Adapter](06-adapter.md)
