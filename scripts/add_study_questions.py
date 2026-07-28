#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "bytebytego-2025"
VI_DIR = OUTPUT_ROOT / "vi"
MANIFEST_PATH = OUTPUT_ROOT / "manifest" / "articles.json"
SECTION_HEADING = "## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ"
OLD_SECTION_HEADINGS = [
    "## Câu hỏi ôn tập + trả lời + thinking",
    SECTION_HEADING,
]
SECTION_NOTE = (
    "Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc và được trả lời trực tiếp; "
    "nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra."
)


@dataclass(frozen=True)
class TopicProfile:
    name: str
    keywords: tuple[str, ...]
    additions: tuple[str, ...]
    decision_lens: str
    connection: str


TOPIC_PROFILES = [
    TopicProfile(
        name="algorithm",
        keywords=("algorithm", "thuật toán", "data structure", "hashmap", "coding pattern", "dijkstra", "bloom", "consistent hashing"),
        additions=(
            "`A* Search` cho tìm đường có heuristic trong bản đồ/game",
            "`BFS/DFS` cho crawler, dependency graph và duyệt quan hệ",
            "`Consistent Hashing` để phân phối key ổn định trong cache/database cluster",
            "`Bloom Filter` để kiểm tra membership nhanh với bộ nhớ thấp",
            "`Raft/Paxos` cho consensus trong hệ phân tán",
            "`LRU/LFU` cho cache eviction",
            "`MapReduce` cho xử lý dữ liệu lớn theo batch",
            "`Gradient Descent/Backpropagation` cho huấn luyện ML",
        ),
        decision_lens="loại dữ liệu, kích thước input, latency mục tiêu, memory budget và sai số/lỗi có thể chấp nhận",
        connection="Trong project thật, thuật toán thường ẩn sau search, cache, ranking, routing, queue hoặc storage; hiểu nó giúp dự đoán bottleneck trước khi hệ thống lớn lên.",
    ),
    TopicProfile(
        name="api-security-auth",
        keywords=("api", "gateway", "jwt", "oauth", "cookie", "session", "token", "paseto", "authentication", "authorization", "sso", "webauthn", "security", "signature"),
        additions=(
            "idempotency key cho API ghi dữ liệu hoặc payment",
            "OpenAPI/contract validation để giảm sai lệch client-server",
            "correlation id/distributed tracing để debug production",
            "threat modeling theo OWASP API Top 10",
            "secret rotation và key management",
            "policy kiểm tra quyền ở cả Gateway lẫn service boundary",
        ),
        decision_lens="actor, trust boundary, dữ liệu nhạy cảm, lifetime của token/key, quyền truy cập và cơ chế revoke",
        connection="Khi làm API thật, một endpoint chạy được chưa đủ; phải kiểm thêm abuse, audit log, error leakage, rate limit và quyền ở service chứa dữ liệu.",
    ),
    TopicProfile(
        name="database-cache-data",
        keywords=("database", "postgresql", "mysql", "mongodb", "redis", "memcached", "cache", "sql", "query", "index", "shard", "data lake", "data warehouse", "cqrs", "event sourcing"),
        additions=(
            "query plan/EXPLAIN để biết bottleneck thật",
            "transaction isolation để tránh race condition và dirty read",
            "connection pooling/backpressure để database không bị quá tải",
            "cache invalidation strategy rõ ràng",
            "schema migration có rollback",
            "backup/restore drill và data retention policy",
        ),
        decision_lens="read/write ratio, consistency, cardinality, query pattern, growth rate và recovery requirement",
        connection="Khi gặp bài toán dữ liệu, hãy nối bài học với truy vấn nóng nhất, index thật sự được dùng, cache nào có thể stale và thời gian restore sau sự cố.",
    ),
    TopicProfile(
        name="cloud-devops-platform",
        keywords=("kubernetes", "docker", "aws", "cloud", "deployment", "ci/cd", "iac", "infrastructure", "terraform", "cron", "pod", "container", "virtualization", "nginx"),
        additions=(
            "SLO/error budget để biết hệ thống đủ tốt hay chưa",
            "blue-green/canary deployment để giảm rủi ro release",
            "secret management và least privilege IAM",
            "cost monitoring/tagging cho cloud bill",
            "runbook/on-call playbook khi incident xảy ra",
            "policy-as-code cho compliance",
        ),
        decision_lens="độ phức tạp vận hành, rollback, cost, kỹ năng team, observability và blast radius khi hỏng",
        connection="Khi đưa lên production, hãy map từng thành phần vào deploy, rollback, monitoring, alerting, secret, cost và ownership rõ ràng.",
    ),
    TopicProfile(
        name="networking",
        keywords=("http", "https", "tcp", "udp", "dns", "proxy", "router", "firewall", "network", "protocol", "port", "cdn", "tls", "ip address"),
        additions=(
            "DNS caching/TTL và negative caching",
            "TLS handshake/session resumption",
            "CDN edge caching và origin shielding",
            "QUIC/HTTP/3 khi cần giảm latency",
            "packet capture/log correlation khi debug",
            "timeout/retry/backoff policy giữa service",
        ),
        decision_lens="DNS, transport, TLS, HTTP, proxy/CDN, application timeout và observability theo từng layer",
        connection="Khi debug production, hãy tách latency theo DNS lookup, TCP connect, TLS handshake, TTFB và download để không đoán mò.",
    ),
    TopicProfile(
        name="ai-llm-agent",
        keywords=("ai", "llm", "rag", "agent", "mcp", "model", "deepseek", "grok", "transformer", "embedding", "fine-tuning", "lora", "n8n", "langgraph"),
        additions=(
            "evaluation harness để đo chất lượng thay vì cảm tính",
            "guardrails/policy để giảm prompt injection và output nguy hiểm",
            "observability cho prompt, context, latency, cost và hallucination",
            "model routing theo độ khó/cost của request",
            "human-in-the-loop cho tác vụ rủi ro cao",
            "cache embedding/context khi dữ liệu ít đổi",
        ),
        decision_lens="quality, latency, cost/token, privacy, cập nhật tri thức và rủi ro hallucination",
        connection="Khi build AI app, hãy nối model với pipeline thật: data vào đâu, context lấy từ đâu, output được kiểm thế nào và chi phí tăng theo traffic ra sao.",
    ),
    TopicProfile(
        name="architecture-system-design",
        keywords=("architecture", "system design", "scalability", "microservices", "solid", "clean architecture", "domain-driven", "ddd", "monolith", "performance metrics", "latency", "throughput", "design pattern", "nfr", "clean code"),
        additions=(
            "capacity estimation trước khi chọn kiến trúc",
            "SLO/NFR rõ cho latency, availability và durability",
            "graceful degradation khi dependency hỏng",
            "data ownership và service boundary",
            "observability theo RED/USE metrics",
            "ADR để ghi lại trade-off",
        ),
        decision_lens="requirement, constraint, traffic, dữ liệu, failure mode và khả năng vận hành của team",
        connection="Khi gặp system design thật, hãy biến khái niệm thành quyết định: boundary ở đâu, data flow thế nào, bottleneck nào đến trước và rollback ra sao.",
    ),
    TopicProfile(
        name="frontend-productivity",
        keywords=("frontend", "website", "monorepo", "javascript", "typescript", "web application", "url", "clean code"),
        additions=(
            "Core Web Vitals để đo trải nghiệm thật",
            "bundle splitting và lazy loading",
            "design system/component contract",
            "monorepo task caching",
            "accessibility audit",
            "error monitoring phía client",
        ),
        decision_lens="UX, bundle size, build time, maintainability, accessibility và tốc độ release",
        connection="Khi làm frontend production, hãy nối code với người dùng thật: load có nhanh không, lỗi có thấy được không, component có tái dùng được không và build có scale với team không.",
    ),
    TopicProfile(
        name="git-devtools",
        keywords=("git", "github", "branch", "reset", "gitflow", "developer", "testing", "test", "interview"),
        additions=(
            "pre-commit hook/lint để chặn lỗi sớm",
            "trunk-based development khi team cần release nhanh",
            "branch protection và required checks",
            "reflog/revert strategy để cứu lỗi Git",
            "contract test để giảm bug integration",
            "CI cache để rút ngắn feedback loop",
        ),
        decision_lens="feedback loop, rollback, collaboration, code review và mức tự động hóa phù hợp team",
        connection="Khi áp dụng vào team thật, hãy nhìn developer workflow như một hệ thống: commit, review, test, deploy và rollback đều phải giảm rủi ro production.",
    ),
]

DEFAULT_PROFILE = TopicProfile(
    name="general",
    keywords=(),
    additions=(
        "observability để biết hệ thống đang hoạt động thế nào",
        "failure handling để tránh lỗi lan rộng",
        "security/privacy review trước khi production",
        "cost/performance trade-off",
        "documentation/runbook để team vận hành được",
    ),
    decision_lens="problem, input/output, owner, failure mode, cost và cách đo kết quả",
    connection="Khi đọc bài, hãy nối khái niệm với hệ thống thật: ai dùng, dữ liệu đi đâu, lỗi xảy ra ở đâu và đo bằng metric nào.",
)


def clean_question(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^[-*]\s+", "", value)
    value = re.sub(r"^\d+[.)]\s+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -")


def split_questions(value: str) -> list[str]:
    value = clean_question(value)
    if not value:
        return []

    matches = re.findall(r"[^?？]+[?？]", value)
    if matches:
        questions = [clean_question(match) for match in matches]
        remainder = value
        for match in matches:
            remainder = remainder.replace(match, "", 1)
        remainder = clean_question(remainder)
        if remainder and len(remainder.split()) > 3:
            questions.append(remainder)
        return [question for question in questions if question]

    return [value]


def dedupe_questions(questions: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for question in questions:
        normalized = question.casefold().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(question)
    return result


def extract_source_questions(text: str) -> list[str]:
    lines = text.splitlines()
    questions: list[str] = []

    for line_index, line in enumerate(lines):
        match = re.search(r"Câu hỏi dành cho bạn:\s*(.*)", line, flags=re.IGNORECASE)
        if not match:
            continue

        questions.extend(split_questions(match.group(1)))
        cursor = line_index + 1
        while cursor < len(lines):
            current = lines[cursor].strip()
            if current.startswith("## "):
                break
            if current:
                looks_like_question_item = bool(re.match(r"^(\d+[.)]|[-*])\s+", current)) or "?" in current
                if looks_like_question_item:
                    questions.extend(split_questions(current))
            cursor += 1

    return dedupe_questions(questions)


def extract_heading_title(text: str) -> str:
    first_line = next((line.strip() for line in text.splitlines() if line.startswith("# ")), "")
    return re.sub(r"^#\s+\d+\s+-\s+", "", first_line).strip() or "bài này"


def extract_section(text: str, heading_pattern: str) -> str:
    match = re.search(
        rf"^## {heading_pattern}.*?\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else ""


def normalize_prose(value: str) -> str:
    value = re.sub(r"\n\s*[-*]\s+", "; ", value)
    value = re.sub(r"\n\s*\d+[.)]\s+", "; ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def truncate_sentence(value: str, limit: int = 520) -> str:
    value = normalize_prose(value)
    if len(value) <= limit:
        return value

    cut = value[:limit].rsplit(" ", 1)[0].rstrip(" ,;:")
    return f"{cut}..."


def summary_answer_source(text: str) -> str:
    summary = extract_section(text, r"Tóm tắt")
    if not summary:
        summary = extract_section(text, r"Dịch sát")

    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", summary) if paragraph.strip()]
    if not paragraphs:
        return "Bài này cần được đọc lại cùng hình minh họa để rút ra ý chính trước khi trả lời."

    useful: list[str] = []
    for paragraph in paragraphs:
        normalized = normalize_prose(paragraph)
        if not normalized:
            continue
        if normalized.endswith(":") and len(useful) >= 1:
            continue
        useful.append(normalized.rstrip(":"))
        if len(" ".join(useful)) >= 260:
            break
    return truncate_sentence(" ".join(useful), limit=520)


def extract_terms(text: str) -> list[str]:
    terms_section = extract_section(text, r"Thuật ngữ chính")
    terms = re.findall(r"^- `([^`]+)`:" , terms_section, flags=re.MULTILINE)
    if not terms:
        terms = re.findall(r"^[-*]\s+`([^`]+)`", terms_section, flags=re.MULTILINE)
    return terms[:5]


def detect_profile(title: str, original_title: str, terms: list[str], text: str) -> TopicProfile:
    title_haystack = " ".join([title, original_title]).casefold()
    terms_haystack = " ".join(terms).casefold()
    body_haystack = text[:2500].casefold()
    best_profile = DEFAULT_PROFILE
    best_score = 0
    for profile in TOPIC_PROFILES:
        score = 0
        for keyword in profile.keywords:
            normalized = keyword.casefold()
            if normalized in title_haystack:
                score += 5
            if normalized in terms_haystack:
                score += 3
            if normalized in body_haystack:
                score += 1
        if score > best_score:
            best_profile = profile
            best_score = score
    return best_profile


def format_items(items: tuple[str, ...], count: int = 4) -> str:
    selected = list(items[:count])
    if len(selected) == 1:
        return selected[0]
    return "; ".join(selected[:-1]) + "; và " + selected[-1]


def pick_variant(seed: str, variants: tuple[str, ...]) -> str:
    return variants[sum(ord(char) for char in seed) % len(variants)]


def question_kind(question: str) -> str:
    lower_question = question.casefold()
    if any(marker in lower_question for marker in ["bỏ sót", "thêm gì", "thêm ", "add ", "cách nào khác", "nào khác", "gì khác", "best practice nào khác", "service nào khác", "tool nào khác", "resource nào khác", "chiến lược nào khác", "pattern nào khác", "khái niệm nào khác"]):
        return "add"
    if any(marker in lower_question for marker in ["đã dùng", "có dùng", "đã thử", "từng gặp", "yêu thích", "dự định dùng", "đã khám phá"]):
        return "experience"
    if any(marker in lower_question for marker in ["khác nhau", "difference", " vs ", "versus", "so với"]):
        return "compare"
    if any(marker in lower_question for marker in ["có cần", "should we", "nên dùng", "nên chọn", "which one"]):
        return "decision"
    if any(marker in lower_question for marker in ["hạn chế", "challenge", "overhead", "rủi ro"]):
        return "limit"
    if any(marker in lower_question for marker in ["như thế nào", "hoạt động", "làm sao", "how", "process", "flow"]):
        return "how"
    return "general"


def special_answer(question: str, title: str, key_idea: str) -> str | None:
    lower_question = question.casefold()
    lower_title = title.casefold()

    if "thuật toán phổ biến" in lower_question and "bỏ sót" in lower_question:
        return (
            "Có. Nếu mở rộng danh sách, các thuật toán/pattern rất đáng thêm là `A* Search` cho tìm đường có heuristic, `BFS/DFS` cho duyệt graph, "
            "`Consistent Hashing` cho cache/database cluster, `Bloom Filter` cho kiểm tra membership nhanh, `Raft/Paxos` cho consensus, "
            "`LRU/LFU` cho cache eviction, `MapReduce` cho xử lý dữ liệu lớn và `Gradient Descent/Backpropagation` cho ML. "
            "Những mục này bổ sung các mảng mà bài gốc mới chạm một phần: distributed systems, cache, big data và machine learning training."
        )

    if "load balancer" in lower_question and "api gateway" in lower_question:
        return (
            "Load balancer chủ yếu phân phối traffic giữa nhiều instance/server để tăng availability và throughput. "
            "API Gateway đứng ở tầng API nên xử lý nhiều logic hơn: authentication, authorization, rate limit, routing theo path/version, logging, caching và protocol conversion. "
            "Trong kiến trúc production, hai lớp này thường đi cùng nhau: load balancer đưa traffic tới cụm gateway, gateway mới quyết định request đi tới service nào."
        )

    if "api gateway" in lower_question and any(client_word in lower_question for client_word in ["mobile", "browser", "pc"]):
        return (
            "Không bắt buộc tách ngay. Nếu Web, Mobile và PC dùng policy gần giống nhau, một API Gateway chung sẽ đơn giản và dễ vận hành hơn. "
            "Chỉ nên tách gateway/BFF riêng khi mỗi client có nhu cầu khác rõ: payload aggregation riêng, auth flow riêng, rate limit riêng, versioning riêng hoặc release cadence khác nhau."
        )

    if "qr code login" in lower_question:
        return (
            "QR code login thường hoạt động bằng cách browser/TV tạo một login session tạm thời và hiển thị mã QR chứa `login_token` hoặc URL xác thực ngắn hạn. "
            "Mobile app đã đăng nhập quét mã, gửi token đó lên server để xác nhận danh tính. Server đánh dấu session trên browser/TV là authenticated, rồi thiết bị kia tự polling hoặc nhận realtime event để chuyển sang trạng thái đã đăng nhập. "
            "Điểm quan trọng là token phải ngắn hạn, dùng một lần và bị ràng buộc với session/device ban đầu."
        )

    if "jwt" in (lower_question + " " + title.casefold()) and "khi nào" in lower_question and "authentication" in lower_question:
        return (
            "Nên dùng JWT khi hệ thống cần stateless authentication cho API/mobile/SPA, có nhiều backend service cùng verify token, traffic cao và chấp nhận mô hình access token ngắn hạn. "
            "Không nên dùng JWT như session dài hạn nếu cần revoke tức thì, kiểm soát trạng thái đăng nhập chặt hoặc lưu dữ liệu nhạy cảm trong token. Trong các case đó, server-side session, token introspection hoặc access token ngắn hạn + refresh token sẽ an toàn/dễ kiểm soát hơn."
        )

    if "authentication" in lower_question and "nào khác" in lower_question:
        return (
            "Ngoài JWT, các lựa chọn authentication/authentication-related phổ biến gồm server-side session bằng cookie, OAuth2/OIDC cho đăng nhập qua identity provider, SSO cho doanh nghiệp, API key cho machine-to-machine đơn giản, mTLS cho service nội bộ cần xác thực hai chiều, WebAuthn/passkey cho login chống phishing và PASETO nếu muốn token có mặc định crypto an toàn hơn JWT. "
            "Chọn cách nào phụ thuộc client là browser/mobile/service, yêu cầu revoke, mức nhạy cảm dữ liệu và khả năng vận hành key/session store."
        )

    if "digital signature" in lower_question:
        return (
            "Digital signature rất nên dùng khi cần chứng minh dữ liệu đến từ đúng nguồn và không bị sửa: ký JWT/JWS, ký webhook payload, ký release artifact, ký tài liệu pháp lý hoặc ký request giữa service. "
            "Nó khác encryption ở chỗ mục tiêu chính không phải giấu nội dung, mà là xác minh tính toàn vẹn và nguồn gốc bằng public key."
        )

    if "sensitive user data" in lower_question and "cache" in lower_question:
        return (
            "Muốn xóa sensitive data khỏi nhiều tầng cache thì không thể chỉ xóa một key ở Redis. Cần thiết kế data classification, key naming nhất quán, TTL ngắn cho dữ liệu nhạy cảm, cache purge theo user/object id, event invalidation tới CDN/app/browser cache, và không cache PII khi không thật cần. "
            "Với dữ liệu bắt buộc cache, nên encrypt, version key theo policy và có audit log cho lệnh purge để kiểm chứng đã xóa ở các tầng quan trọng."
        )

    if "value object" in lower_question and "equality" in lower_question:
        return (
            "Hai Value Object bằng nhau khi toàn bộ thuộc tính tạo nên giá trị của chúng bằng nhau. Ví dụ `Money(100, 'USD')` bằng một object khác cũng có amount `100` và currency `USD`, dù chúng là hai instance khác nhau. "
            "Vì Value Object không có identity riêng, equality dựa trên value, không dựa trên database id."
        )

    if "entity" in lower_question and "sao" in lower_question:
        return (
            "Hai Entity thường được xem là cùng một thực thể khi chúng có cùng identity, ví dụ cùng `user_id` hoặc `order_id`, kể cả một số field khác đang thay đổi theo thời gian. "
            "Với Entity, equality dựa vào định danh bền vững; còn trạng thái chỉ mô tả phiên bản hiện tại của entity đó."
        )

    if "http status" in lower_question and "category" in lower_question:
        return (
            "Nhóm dễ nhầm nhất thường là `401`, `403`, `409` và `422`. `401` là chưa xác thực hoặc token không hợp lệ; `403` là đã biết bạn là ai nhưng không đủ quyền; `409` là xung đột trạng thái hiện tại của resource; `422` là request đúng syntax nhưng sai rule nghiệp vụ. "
            "Phân biệt đúng các mã này giúp client xử lý retry, login lại, hiển thị lỗi validation hoặc báo conflict chính xác hơn."
        )

    if "solid principle" in lower_question:
        return (
            "Trong thực tế, `Single Responsibility Principle` thường hữu ích nhất vì nó buộc ta tách lý do thay đổi của một class/module. Nguyên tắc khó nhất thường là `Dependency Inversion`, vì muốn làm tốt phải biết đặt boundary, interface và dependency direction đúng. "
            "Nếu áp dụng máy móc, SOLID dễ biến thành quá nhiều abstraction; nếu áp dụng đúng, code dễ test và dễ thay đổi hơn."
        )

    if "layer nào" in lower_question and "testing" in lower_question:
        return (
            "Layer có giá trị nhất thường là integration/contract test, vì nhiều bug production không nằm trong một function riêng lẻ mà nằm ở chỗ các module/service hiểu sai contract của nhau. "
            "Unit test vẫn cần để feedback nhanh, end-to-end test vẫn cần cho flow quan trọng, nhưng integration/contract test thường bắt được lỗi thực tế với chi phí thấp hơn E2E toàn diện."
        )

    if "công ty nào đặt tên tốt nhất" in lower_question:
        return (
            "Nếu xét độ dễ hiểu cho người mới, Google Cloud và Cloudflare thường đặt tên trực quan hơn vì nhiều dịch vụ mô tả khá sát chức năng. AWS phổ biến và giàu dịch vụ nhất, nhưng tên như `S3`, `EC2`, `IAM`, `EKS` cần thời gian học acronym. "
            "Trong team production, tên hay không quan trọng bằng việc mapping đúng service tương đương và hiểu pricing/limit của từng cloud."
        )

    if "grpc" in (lower_question + " " + lower_title) and ("hạn chế" in lower_question or "limit" in lower_question):
        return (
            "gRPC có vài hạn chế rõ: khó debug bằng mắt hơn REST/JSON vì dùng Protobuf binary; browser support không tự nhiên bằng REST nếu không dùng gRPC-Web; schema `.proto` cần quản lý version cẩn thận; load balancer/proxy/observability phải hỗ trợ HTTP/2 tốt; và team cần tooling để inspect request/response. "
            "Vì vậy gRPC hợp cho service-to-service nội bộ hơn là public API cho mọi client."
        )

    if "grpc" in (lower_question + " " + lower_title) and "đã dùng" in lower_question:
        return (
            "Trong một project microservices, gRPC đáng dùng khi các service nội bộ gọi nhau nhiều, cần contract chặt và latency thấp, ví dụ `order-service` gọi `payment-service` hoặc `pricing-service`. "
            "Nếu hệ thống chủ yếu phục vụ browser/public client, REST/JSON vẫn dễ debug và dễ tích hợp hơn; gRPC nên được cân nhắc ở boundary nội bộ nơi Protobuf và HTTP/2 phát huy lợi thế."
        )

    if "deepseek" in lower_question and "đã thử" in lower_question:
        return (
            "DeepSeek đáng thử bằng một benchmark nhỏ thay vì chỉ đọc thông số: chọn vài prompt reasoning, coding, tiếng Việt và RAG nội bộ; đo chất lượng câu trả lời, latency, chi phí/token, mức ổn định và rủi ro dữ liệu. "
            "Nếu kết quả đủ tốt với cost thấp hơn, có thể dùng DeepSeek cho tác vụ ít rủi ro hoặc routing một phần request, còn tác vụ quan trọng vẫn cần model/evaluation đáng tin cậy hơn."
        )

    return None


def special_thinking(question: str, title: str, terms: list[str]) -> str | None:
    lower_question = question.casefold()
    lower_title = title.casefold()
    term_text = ""
    if terms:
        term_text = " Các keyword cần tự giải thích lại: " + ", ".join(f"`{term}`" for term in terms[:5]) + "."

    if "thuật toán phổ biến" in lower_question and "bỏ sót" in lower_question:
        return (
            "Cách nghĩ đúng là phân nhóm thuật toán theo vấn đề hệ thống: graph/search, ranking, cryptography, compression, distributed coordination, cache và ML optimization. "
            "Khi nhìn một sản phẩm thật như map, search engine, CDN hay LLM app, hãy thử chỉ ra thuật toán nào đang quyết định latency, memory và độ chính xác."
            f"{term_text}"
        )

    if "deepseek" in lower_title:
        return (
            "Đừng chỉ hỏi model này có nổi tiếng không; hãy hỏi nó có thắng trên benchmark của chính mình không. "
            "Liên hệ project AI bằng checklist: task nào cho DeepSeek, task nào giữ model khác, dữ liệu có được gửi ra ngoài không, cost/token giảm bao nhiêu và hallucination có tăng không."
            f"{term_text}"
        )

    if "grpc" in lower_title:
        return (
            "gRPC nên được học như một quyết định về contract giữa service, không chỉ là protocol nhanh hơn. "
            "Khi liên hệ project, hãy kiểm boundary public/internal, versioning `.proto`, tracing qua HTTP/2, timeout/retry và khả năng debug khi production incident xảy ra."
            f"{term_text}"
        )

    if "api gateway" in lower_title:
        return (
            "API Gateway là boundary quan trọng, nên thinking phải xoay quanh trách nhiệm nào đặt ở gateway và trách nhiệm nào vẫn phải giữ trong service. "
            "Khi liên hệ project, hãy vẽ đường đi request từ client tới gateway tới microservice, rồi gắn auth, rate limit, logging, cache và circuit breaker vào đúng điểm."
            f"{term_text}"
        )

    if "cache" in lower_title and "sensitive" in lower_question:
        return (
            "Cache làm hệ thống nhanh hơn nhưng cũng tạo bản sao dữ liệu ở nhiều nơi, nên quyền được xóa dữ liệu phải được thiết kế từ đầu. "
            "Khi liên hệ production, hãy inventory mọi cache layer, TTL, key pattern, event invalidation và cách chứng minh purge đã chạy thành công."
            f"{term_text}"
        )

    return None


def answer_for_question(question: str, key_idea: str, title: str, profile: TopicProfile) -> str:
    key_idea = truncate_sentence(key_idea.rstrip(":"), limit=520)
    override = special_answer(question, title, key_idea)
    if override:
        return override

    kind = question_kind(question)
    additions = format_items(profile.additions)

    if kind == "add":
        opener = pick_variant(question + title, (
            "Nên bổ sung",
            "Có thể thêm",
            "Danh sách sẽ đầy đủ hơn nếu thêm",
            "Phần còn thiếu đáng cân nhắc là",
        ))
        return (
            f"{opener} {additions}. "
            f"Các mục này giúp bức tranh đầy đủ hơn vì chúng chạm vào phần triển khai/vận hành mà bài gốc chưa đi sâu. Ý chính đang có của bài là: {key_idea}"
        )

    if kind == "experience":
        opener = pick_variant(question + title, (
            f"Trong project thật, `{title}` đáng dùng/thử khi bài toán khớp với nhu cầu cụ thể và team đo được kết quả.",
            f"Với `{title}`, cách liên hệ tốt nhất là chọn một workload nhỏ rồi kiểm chứng bằng số liệu thay vì chọn theo cảm tính.",
            f"Nếu đưa `{title}` vào stack, nên bắt đầu từ một use case hẹp, dễ rollback và có metric rõ.",
        ))
        return (
            f"{opener} "
            f"Nên kiểm bằng workload nhỏ trước: latency, độ ổn định, khả năng debug, cost và rủi ro vận hành. Phần cốt lõi cần đem theo từ bài là: {key_idea}"
        )

    if kind == "compare":
        return (
            f"Điểm khác nhau nên nhìn từ boundary và trách nhiệm chính. Với `{title}`, hãy tách rõ mỗi bên giải quyết vấn đề gì, dữ liệu đi qua đâu, ai sở hữu state và lỗi sẽ lan như thế nào. "
            f"Ý chính để giữ lại là: {key_idea}"
        )

    if kind == "decision":
        return (
            f"Không nên chọn theo tên công nghệ. Với `{title}`, quyết định nên dựa vào {profile.decision_lens}. "
            f"Nếu nhu cầu thật khớp với lợi ích trong bài thì dùng; nếu không, giữ phương án đơn giản hơn. Ý chính là: {key_idea}"
        )

    if kind == "limit":
        return (
            f"Hạn chế cần soi ở các điểm: {profile.decision_lens}. "
            f"Khi áp dụng `{title}` vào production, hãy đo trước rủi ro vận hành thay vì chỉ nhìn ưu điểm trên diagram. Ý chính của bài là: {key_idea}"
        )

    if kind == "how":
        opener = pick_variant(question + title, (
            "Luồng tốt nhất là lần theo input tới output",
            "Nên trả lời theo flow end-to-end",
            "Hãy tách flow thành các bước có state rõ ràng",
        ))
        return (
            f"{opener}: request/dữ liệu đi vào đâu, qua thành phần nào, state đổi ở đâu và kết quả trả ra thế nào. "
            f"Với `{title}`, ý chính là: {key_idea}"
        )

    opener = pick_variant(question + title, (
        "Bài này muốn người đọc nắm",
        "Trọng tâm cần đem vào thực tế là",
        "Sau bài này, phần đáng nhớ nhất là",
        "Nếu rút thành checklist thiết kế thì ý chính là",
    ))
    return (
        f"{opener}: {key_idea} "
        f"Khi áp dụng vào hệ thống thật, hãy kiểm thêm {profile.decision_lens}."
    )


def thinking_for_question(question: str, title: str, terms: list[str], profile: TopicProfile) -> str:
    override = special_thinking(question, title, terms)
    if override:
        return override

    kind = question_kind(question)
    if kind == "add":
        opener = pick_variant(question + title, (
            f"Danh sách trong `{title}` nên được kiểm theo coverage: nó đã nói phần nào, thiếu phần nào và phần thiếu có làm thay đổi quyết định thiết kế không.",
            f"Khi bài hỏi còn thiếu gì trong `{title}`, hãy so danh sách hiện tại với nhu cầu production: scale, debug, security, cost và vận hành.",
            f"Đừng thêm mục cho dài danh sách; với `{title}`, chỉ thêm thứ mở ra một nhóm vấn đề mới hoặc giúp ra quyết định thiết kế tốt hơn.",
        ))
    elif kind == "experience":
        opener = pick_variant(question + title, (
            f"Câu hỏi trải nghiệm trong `{title}` nên quy về adoption: dùng cho workload nào, đo thành công bằng metric nào và có đáng giữ lâu dài trong stack không.",
            f"Khi tự liên hệ `{title}`, hãy viết ra một project cụ thể, lý do chọn công nghệ và lỗi vận hành có thể xảy ra.",
            f"Với `{title}`, trải nghiệm thật nên được đo bằng latency, độ ổn định, chi phí, khả năng debug và mức dễ rollback.",
        ))
    elif kind == "compare":
        opener = f"Khi so sánh trong `{title}`, hãy tách responsibility, boundary, state, failure mode và cost vận hành thay vì chỉ so tên công nghệ."
    elif kind == "decision":
        opener = f"Quyết định trong `{title}` chỉ có ý nghĩa khi nêu được điều kiện dùng, điều kiện không dùng và tín hiệu nào chứng minh lựa chọn đang đúng."
    elif kind == "limit":
        opener = f"Hạn chế của `{title}` thường xuất hiện ở phần ít thấy trên diagram: debug, rollout, compatibility, cost hoặc security."
    elif kind == "how":
        opener = f"Luồng trong `{title}` nên được vẽ từ input tới output, kèm owner của từng bước và failure mode ở mỗi boundary."
    else:
        opener = pick_variant(question + title, (
            f"Ôn tập `{title}` bằng cách biến khái niệm thành quyết định thiết kế cụ thể: chọn gì, bỏ gì, đo gì và ai chịu trách nhiệm.",
            f"Khi học `{title}`, hãy thử viết một checklist áp dụng vào project: input, output, owner, rủi ro và metric kiểm chứng.",
            f"Liên hệ `{title}` bằng một scenario thật sẽ giúp thấy trade-off rõ hơn so với chỉ đọc định nghĩa.",
        ))

    term_text = ""
    if terms:
        term_text = " Khi ghi chú lại, hãy giải thích được các keyword: " + ", ".join(f"`{term}`" for term in terms[:5]) + "."

    return (
        f"{opener} Lens chính là {profile.decision_lens}. "
        f"{profile.connection}"
        f"{term_text}"
    )


def fallback_question(title: str, original_title: str) -> str:
    if "?" in original_title:
        return original_title
    if "?" in title:
        return title
    return f"Sau khi đọc bài “{original_title or title}”, ý chính cần trả lời và áp dụng vào system design là gì?"


def strip_existing_question_section(text: str) -> str:
    for heading in OLD_SECTION_HEADINGS:
        marker = f"\n{heading}\n"
        if marker in text:
            return text.split(marker, 1)[0].rstrip() + "\n"
    return text.rstrip() + "\n"


def build_question_section(
    *,
    text: str,
    title: str,
    original_title: str,
    source_questions: list[str],
) -> str:
    key_idea = summary_answer_source(text)
    terms = extract_terms(text)
    profile = detect_profile(title, original_title, terms, text)
    questions = source_questions or [fallback_question(title, original_title)]
    source_label = "Câu hỏi trong tài liệu gốc." if source_questions else "Suy ra từ tiêu đề/nội dung chính vì bài gốc không có câu hỏi riêng."

    lines = ["", SECTION_HEADING, "", f"> {SECTION_NOTE}", ""]
    for question_index, question in enumerate(questions, start=1):
        lines.extend([
            f"### Câu hỏi {question_index}",
            "",
            f"**Nguồn câu hỏi:** {source_label}",
            "",
            f"**Câu hỏi:** {question}",
            "",
            f"**Trả lời:** {answer_for_question(question, key_idea, title, profile)}",
            "",
            f"**Thinking học tập + liên hệ:** {thinking_for_question(question, title, terms, profile)}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    original_titles = {
        Path(article["vi_path"]).name: article["title"]
        for article in manifest["articles"]
    }

    updated = 0
    explicit_question_files = 0
    fallback_question_files = 0
    total_questions = 0

    for markdown_path in sorted(VI_DIR.glob("*.md")):
        if markdown_path.name.startswith("000-"):
            continue

        text = markdown_path.read_text()
        base_text = strip_existing_question_section(text)
        title = extract_heading_title(base_text)
        original_title = original_titles.get(markdown_path.name, title)
        source_questions = extract_source_questions(base_text)
        if source_questions:
            explicit_question_files += 1
        else:
            fallback_question_files += 1

        question_section = build_question_section(
            text=base_text,
            title=title,
            original_title=original_title,
            source_questions=source_questions,
        )
        markdown_path.write_text(base_text + question_section)
        updated += 1
        total_questions += len(source_questions) or 1

    print(f"updated={updated}")
    print(f"explicit_question_files={explicit_question_files}")
    print(f"fallback_question_files={fallback_question_files}")
    print(f"total_question_blocks={total_questions}")


if __name__ == "__main__":
    main()
