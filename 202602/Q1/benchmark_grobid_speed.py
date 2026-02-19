import statistics
import time
from pathlib import Path

from grobid_client.grobid_client import GrobidClient


def run_once(
    client: GrobidClient,
    input_dir: Path,
    output_dir: Path,
    n_concurrent: int,
) -> float:
    """
    한 번의 실행에서 `input_dir` 내 PDF들을 처리하고 걸린 시간을 초 단위로 반환합니다.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"입력 폴더가 없습니다: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    start = time.perf_counter()

    client.process(
        service="processFulltextDocument",
        input_path=str(input_dir),
        output=str(output_dir),
        n=n_concurrent,
    )

    return time.perf_counter() - start


def main() -> None:
    """
    같은 10개의 PDF를 10번 반복 처리하여 실행 시간과 평균 속도를 계산합니다.
    - 입력 폴더: 202602/Q1/input_pdfs
    - 출력 폴더: 202602/Q1/benchmark_outputs/run_{i}
    """
    base_dir = Path(__file__).resolve().parent

    # 설정값 (`convert_pdfs_to_xml.py`와 동일한 기준 경로 사용)
    input_dir = base_dir / "input_pdfs"
    benchmark_base_output = base_dir / "benchmark_outputs"
    docs_per_run = 10
    num_runs = 10
    n_concurrent = 2  # GrobidClient에서 사용할 동시 처리 쓰레드 수

    # 실제로 처리할 PDF 개수 확인 (부족하면 에러)
    pdf_files = sorted(input_dir.glob("*.pdf"))
    if len(pdf_files) < docs_per_run:
        raise ValueError(
            f"PDF 파일이 {docs_per_run}개보다 적습니다. "
            f"현재 개수: {len(pdf_files)}"
        )

    # GROBID 클라이언트 (서버는 기본 http://localhost:8070 가정)
    client = GrobidClient()

    runtimes: list[float] = []

    total_docs = docs_per_run * num_runs

    for i in range(1, num_runs + 1):
        run_output_dir = benchmark_base_output / f"run_{i}"
        elapsed = run_once(
            client=client,
            input_dir=input_dir,
            output_dir=run_output_dir,
            n_concurrent=n_concurrent,
        )
        runtimes.append(elapsed)

        docs_per_second = docs_per_run / elapsed
        seconds_per_doc = elapsed / docs_per_run

        print(
            f"[Run {i}] {docs_per_run}개 문서 처리: "
            f"{elapsed:.2f}초, "
            f"{docs_per_second:.2f} 문서/초, "
            f"{seconds_per_doc:.2f} 초/문서"
        )

    total_time = sum(runtimes)
    avg_time = statistics.mean(runtimes)

    avg_docs_per_second = total_docs / total_time
    avg_seconds_per_doc = total_time / total_docs

    print("\n=== 요약 ===")
    print(f"총 실행 횟수: {num_runs}회")
    print(f"한 번에 처리한 문서 수: {docs_per_run}개")
    print(f"총 처리 문서 수: {total_docs}개")
    print(f"총 처리 시간(합계): {total_time:.2f}초")
    print(f"실행당 평균 시간: {avg_time:.2f}초")
    print(f"평균 속도: {avg_docs_per_second:.2f} 문서/초")
    print(f"평균 처리 시간: {avg_seconds_per_doc:.2f} 초/문서")


if __name__ == "__main__":
    main()