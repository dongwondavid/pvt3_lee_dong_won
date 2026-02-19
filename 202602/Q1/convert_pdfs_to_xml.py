import time
from pathlib import Path

from grobid_client.grobid_client import GrobidClient


def main() -> None:
    """
    `input_pdfs` 폴더 안의 모든 PDF를 GROBID를 이용해 TEI XML로 변환하고,
    결과를 `output_xmls` 폴더에 저장한 뒤 총 소요 시간을 출력합니다.
    """
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input_pdfs"
    output_dir = base_dir / "output_xmls"

    if not input_dir.exists():
        raise FileNotFoundError(f"입력 폴더가 없습니다: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    # GROBID 서버가 기본값(http://localhost:8070)에서 동작한다고 가정합니다.
    # 다른 서버를 사용하려면 grobid_server 인자를 넘겨서 초기화하세요.
    # 예: GrobidClient(grobid_server="http://your-grobid-server:8070")
    client = GrobidClient()

    start = time.perf_counter()

    # processFulltextDocument 서비스로 PDF 전체 텍스트를 TEI XML로 변환
    client.process(
        service="processFulltextDocument",
        input_path=str(input_dir),
        output=str(output_dir),
        n=10,  # 동시에 처리할 작업 수 (환경에 맞게 조정 가능)
    )

    elapsed = time.perf_counter() - start

    print(f"총 처리 시간: {elapsed:.2f}초")


if __name__ == "__main__":
    main()

