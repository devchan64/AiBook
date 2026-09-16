#!/usr/bin/env python3
"""폐기 확정 목표 후보를 제외하고 생성한다.

--dry-run으로 실행 대상과 제외 ID를 확인한다. 원래 생성 조건은 보존한다.
"""
from p7_5_10_generate_reviewed_inputs import main


if __name__ == '__main__':
    main(policy_name='p7-5-10-target-generation-exclusions.json',
         spec_name='p7-5-10-mira-target-pool-v3.json', output_name='target-images')
