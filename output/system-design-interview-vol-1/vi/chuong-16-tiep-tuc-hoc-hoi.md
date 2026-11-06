# Chương 16: Tiếp tục học hỏi

[English](../original/chuong-16-tiep-tuc-hoc-hoi.md) · [Mục lục](../README.md)

*Tên gốc: The Learning Continues. Nguồn: trang PDF 264-268. Các URL bên dưới được giữ theo nguồn; tên gốc của tài liệu được giữ kèm tên dịch khi cần tra cứu.*

<!-- trang-pdf:264 -->

Thiết kế hệ thống tốt đòi hỏi nhiều năm tích lũy kiến thức. Một con đường rút ngắn là tìm hiểu sâu kiến trúc của các hệ thống thực tế. Dưới đây là tập hợp những tài liệu hữu ích. Chúng tôi đặc biệt khuyến khích bạn chú ý cả những nguyên tắc chung lẫn các công nghệ bên dưới. Nghiên cứu từng công nghệ và hiểu nó giải quyết vấn đề gì là cách rất tốt để củng cố nền tảng kiến thức và hoàn thiện quá trình thiết kế.

<!-- trang-pdf:265 -->

## Các hệ thống thực tế

Những tài liệu sau giúp bạn hiểu các ý tưởng thiết kế tổng quát của kiến trúc hệ thống thực tế tại nhiều công ty.

- **Facebook Timeline: Sức mạnh của phi chuẩn hóa** (*Facebook Timeline: Brought To You By The Power Of Denormalization*): https://goo.gl/FCNrbm
- **Quy mô tại Facebook** (*Scale at Facebook*): https://goo.gl/NGTdCs
- **Xây dựng Timeline: Mở rộng để chứa câu chuyện cuộc đời bạn** (*Building Timeline: Scaling up to hold your life story*): https://goo.gl/8p5wDV
- **Erlang tại Facebook, Facebook Chat** (*Erlang at Facebook*): https://goo.gl/zSLHrj
- **Facebook Chat:** https://goo.gl/qzSiWC
- **Tìm kim trong Haystack: Hệ thống lưu ảnh của Facebook** (*Finding a needle in Haystack: Facebook’s photo storage*): https://goo.gl/edj4FL
- **Phục vụ Facebook Multifeed: Tăng hiệu quả và hiệu năng nhờ thiết kế lại** (*Serving Facebook Multifeed: Efficiency, performance gains through redesign*): https://goo.gl/adFVMQ
- **Mở rộng Memcache tại Facebook** (*Scaling Memcache at Facebook*): https://goo.gl/rZiAhX
- **TAO: Kho dữ liệu phân tán của Facebook cho đồ thị xã hội** (*TAO: Facebook’s Distributed Data Store for the Social Graph*): https://goo.gl/Tk1DyH
- **Kiến trúc Amazon** (*Amazon Architecture*): https://goo.gl/k4feoW
- **Dynamo: Kho khóa-giá trị có tính sẵn sàng cao của Amazon** (*Dynamo: Amazon’s Highly Available Key-value Store*): https://goo.gl/C7zxDL
- **Góc nhìn 360 độ về toàn bộ ngăn xếp Netflix** (*A 360 Degree View Of The Entire Netflix Stack*): https://goo.gl/rYSDTz
- **Tất cả xoay quanh kiểm thử A/B: Nền tảng thử nghiệm Netflix** (*It’s All A/Bout Testing: The Netflix Experimentation Platform*): https://goo.gl/agbA4K
- **Đề xuất Netflix: Vượt ra ngoài thang 5 sao, phần 1** (*Netflix Recommendations: Beyond the 5 stars, Part 1*): https://goo.gl/A4FkYi
- **Đề xuất Netflix: Vượt ra ngoài thang 5 sao, phần 2** (*Netflix Recommendations: Beyond the 5 stars, Part 2*): https://goo.gl/XNPMXm
- **Kiến trúc Google** (*Google Architecture*): https://goo.gl/dvkDiY
- **Hệ thống tệp Google, tài liệu Google Docs** (*The Google File System, Google Docs*): https://goo.gl/xj5n9R
- **Đồng bộ vi sai, tài liệu Google Docs** (*Differential Synchronization, Google Docs*): https://goo.gl/9zqG7x
- **Kiến trúc YouTube** (*YouTube Architecture*): https://goo.gl/mCPRUF
- **Hội nghị Seattle về khả năng mở rộng: Khả năng mở rộng của YouTube** (*Seattle Conference on Scalability: YouTube Scalability*): https://goo.gl/dH3zYq
- **Bigtable: Hệ thống lưu trữ phân tán cho dữ liệu có cấu trúc** (*Bigtable: A Distributed Storage System for Structured Data*): https://goo.gl/6NaZca
- **Kiến trúc Instagram: 14 triệu người dùng, hàng terabyte ảnh, hàng trăm instance, hàng chục công nghệ** (*Instagram Architecture: 14 Million Users, Terabytes Of Photos, 100s Of Instances, Dozens Of Technologies*): https://goo.gl/s1VcW5
- **Kiến trúc Twitter dùng để phục vụ 150 triệu người dùng hoạt động** (*The Architecture Twitter Uses To Deal With 150M Active Users*): https://goo.gl/EwvfRd
- **Mở rộng Twitter: Làm Twitter nhanh hơn 10.000%** (*Scaling Twitter: Making Twitter 10000 Percent Faster*): https://goo.gl/nYGC1k
- **Giới thiệu Snowflake** (*Announcing Snowflake*). Snowflake là dịch vụ mạng sinh ID duy nhất ở quy mô lớn với một số bảo đảm đơn giản: https://goo.gl/GzVWYm
- **Timeline ở quy mô lớn** (*Timelines at Scale*): https://goo.gl/8KbqTy
- **Uber mở rộng nền tảng thị trường thời gian thực như thế nào** (*How Uber Scales Their Real-Time Market Platform*): https://goo.gl/kGZuVy
- **Mở rộng Pinterest** (*Scaling Pinterest*): https://goo.gl/KtmjW3
- **Cập nhật kiến trúc Pinterest** (*Pinterest Architecture Update*): https://goo.gl/w6rRsf

<!-- trang-pdf:266 -->

- **Lược sử mở rộng LinkedIn** (*A Brief History of Scaling LinkedIn*): https://goo.gl/8A1Pi8
- **Kiến trúc Flickr** (*Flickr Architecture*): https://goo.gl/dWtgYa
- **Chúng tôi đã mở rộng Dropbox như thế nào** (*How We’ve Scaled Dropbox*): https://goo.gl/NjBDtC
- **Kiến trúc WhatsApp mà Facebook mua với giá 19 tỷ USD** (*The WhatsApp Architecture Facebook Bought For $19 Billion*): https://bit.ly/2AHJnFn

<!-- trang-pdf:267 -->

## Blog kỹ thuật của các công ty

Nếu sắp phỏng vấn tại một công ty, đọc blog kỹ thuật của họ để làm quen với các công nghệ và hệ thống được áp dụng, triển khai ở đó là một ý tưởng hay. Ngoài ra, blog kỹ thuật mang lại những hiểu biết vô giá trong các lĩnh vực cụ thể. Đọc thường xuyên có thể giúp chúng ta trở thành kỹ sư tốt hơn.

Dưới đây là danh sách blog kỹ thuật của một số công ty lớn và startup nổi tiếng:

- **Airbnb:** https://medium.com/airbnb-engineering
- **Amazon:** https://developer.amazon.com/blogs
- **Asana:** https://blog.asana.com/category/eng
- **Atlassian:** https://developer.atlassian.com/blog
- **Bittorrent:** http://engineering.bittorrent.com
- **Cloudera:** https://blog.cloudera.com
- **Docker:** https://blog.docker.com
- **Dropbox:** https://blogs.dropbox.com/tech
- **eBay:** http://www.ebaytechblog.com
- **Facebook:** https://code.facebook.com/posts
- **GitHub:** https://githubengineering.com
- **Google:** https://developers.googleblog.com
- **Groupon:** https://engineering.groupon.com
- **Highscalability:** http://highscalability.com
- **Instacart:** https://tech.instacart.com
- **Instagram:** https://engineering.instagram.com
- **LinkedIn:** https://engineering.linkedin.com/blog
- **Mixpanel:** https://mixpanel.com/blog
- **Netflix:** https://medium.com/netflix-techblog
- **Nextdoor:** https://engblog.nextdoor.com
- **PayPal:** https://www.paypal-engineering.com
- **Pinterest:** https://engineering.pinterest.com
- **Quora:** https://engineering.quora.com
- **Reddit:** https://redditblog.com
- **Salesforce:** https://developer.salesforce.com/blogs/engineering
- **Shopify:** https://engineering.shopify.com
- **Slack:** https://slack.engineering
- **SoundCloud:** https://developers.soundcloud.com/blog
- **Spotify:** https://labs.spotify.com
- **Stripe:** https://stripe.com/blog/engineering
- **System design primer:** https://github.com/donnemartin/system-design-primer
- **Twitter:** https://blog.twitter.com/engineering/en_us.html
- **Thumbtack:** https://www.thumbtack.com/engineering
- **Uber:** http://eng.uber.com

<!-- trang-pdf:268 -->

- **Yahoo:** https://yahooeng.tumblr.com
- **Yelp:** https://engineeringblog.yelp.com
- **Zoom:** https://medium.com/zoom-developer-blog

---

[← Chương 15](chuong-15-thiet-ke-google-drive.md) · [Mục lục](../README.md) · [Lời kết →](17-loi-ket.md)
