# Hướng dẫn đóng góp

[![English](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/en/outline.svg)](CONTRIBUTING.en.md)
[![한국어](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ko/outline.svg)](CONTRIBUTING.ko.md)
[![Español](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/es/outline.svg)](CONTRIBUTING.es.md)
[![Tiếng Việt](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/vi/flat.svg)](CONTRIBUTING.vi.md)
[![العربية](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/ar/outline.svg)](CONTRIBUTING.ar.md)
[![Français](https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges/lang/fr/outline.svg)](CONTRIBUTING.fr.md)

<!-- work-only:start -->
## Nhánh

| Nhánh | Mục đích |
| --- | --- |
| `main` | Bản sao chính xác của [eGovFramework/homebrew-egovframe](https://github.com/eGovFramework/homebrew-egovframe). Được đồng bộ hằng ngày, không bao giờ commit vào đây. |
| `work` | Nhánh mặc định. Chứa các thay đổi riêng của bản fork này: CI, tự động hóa, tài liệu và sửa lỗi cask. Hãy mở pull request vào nhánh này. |
| `upstream-submit` | Commit sẵn sàng gửi lên kho chính thức, dựa trên `main` chính thức; tự động cập nhật sau khi CI của `work` thành công và không có PR nào đang mở tới kho chính thức. |
| `upstream-submit-*` | Các bản chụp dùng một lần do `scripts/open_upstream_pr.sh` tạo ra; tách biệt với nhánh gửi cố định. |

`main` là bản sao của kho chính thức nên không commit trực tiếp vào đó. Hãy gửi thay đổi vào nhánh mặc định `work`.

Chi tiết vận hành, lịch chạy và việc bổ sung Release cũ: [MAINTENANCE.md](../../.github/MAINTENANCE.md).
<!-- work-only:end -->

## Trước khi mở pull request

```bash
python3 -m pip install PyYAML==6.0.3
python3 -m unittest discover -s tests -v   # kiểm thử các script
brew style leejongyoung/egovframe/egovframedev-latest   # cần có tap: brew tap leejongyoung/egovframe
```

CI (`ci.yml`) chạy các kiểm thử cùng với `scripts/check_tap.sh` (`brew readall`, `brew style` và `brew audit`). Hãy chạy các lệnh từ thư mục gốc của kho; kiểm thử script cần PyYAML, và CI cài đặt theo cùng cách.

- Thông điệp commit theo phong cách đã dùng ở kho chính thức: `feat(casks): add egovframedev@X.Y.Z`, `fix(casks): …`, `docs(readme): …`, `ci: …`.
- Không sửa tay SHA-256 của cask. Phiên bản mới được tạo bởi `scripts/update_casks.py` (quy trình `Update casks`); để kiểm tra lại một hash hiện có, chạy `gh workflow run update-casks.yml -f verify=<version>`.
- Mỗi dòng phiên bản phụ chỉ giữ một cask: khi thêm `5.0.3` thì xóa `5.0.2` (cùng quy ước với kho chính thức).

## GitHub Actions và chi phí

- **Miễn phí trên kho công khai:** theo chính sách thanh toán của GitHub, các runner tiêu chuẩn do GitHub lưu trữ (`ubuntu-latest`, `macos-latest`) **miễn phí và không giới hạn số phút trên kho công khai**. Các tệp DMG được tính hash theo luồng trong `update-casks.yml` và không bao giờ được tải lên dưới dạng artifact của Actions hay tài sản của Release, nên cũng không tốn dung lượng lưu trữ của Actions.
- Số phút chỉ bị trừ vào hạn mức miễn phí của tài khoản nếu bạn sao chép kho sang kho riêng tư và chạy ở đó.

<!-- work-only:start -->
## Gửi thay đổi lên kho chính thức

Hãy dùng script thay vì đẩy trực tiếp `work`. Script tạo một commit sạch trên nhánh của kho chính thức từ phần khác biệt giữa kho chính thức và `work`, đồng thời bỏ qua các tệp chỉ dành cho fork (`.github/MAINTENANCE.md`, `.github/UPSTREAM_PR.md`, `.github/workflows/sync-upstream.yml`, `scripts/open_upstream_pr.sh`, `tests/test_open_upstream_pr.py` và các khối đánh dấu `work-only`):

```bash
scripts/open_upstream_pr.sh --dry-run                        # xem trước nội dung sẽ gửi
scripts/open_upstream_pr.sh -m "fix(casks): use depends_on :macos" --only Casks
```
<!-- work-only:end -->

## Bảo mật

Không báo cáo lỗ hổng bảo mật qua issue; hãy làm theo quy trình trong [SECURITY.vi.md](../security/SECURITY.vi.md).
