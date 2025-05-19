# TITLE
본 프로젝트는 글로벌 시장 진출 전략 에이전트를 설계하고 구현한 실습 프로젝트입니다.

## Overview

- 프로젝트 목적 : 글로벌 시장으로의 진출을 목표로 하고 있는 국내 AI 스타트업에게 글로벌 진출 전략을 제공합니다.
                 AI 에이전트의 신속,정확한 전략 제안을 기반으로 의사 결정에 투입되는 비용을 효과적으로 절감하고자 합니다.  
- 수행 방안 : 멀티 에이전트 기반 RAG 
- Tools : 웹 스크래핑, LLM 기반 요약/분석, PDF/문서 정보 추출, 정보 정합성/스코어링, 에이전트 프레임워크 

## Features

- 멀티 에이전트 기반 글로벌 시장·기업 분석 자동화: 다양한 AI 에이전트가 시장(PESTEL), 기업(SWOT), 경쟁사, 파트너사 등 각종 정보를 웹 스크래핑과 LLM 기반으로 신속·정확하게 분석합니다
- 정량적 평가 및 진출 최적 지역 자동 추천: 분석 결과를 벡터 DB에 저장하고, 정보 정합성·스코어링 알고리즘을 통해 진출에 가장 적합한 국가/지역을 자동으로 선정합니다.
- 전략 종합 보고서 자동 생성 및 문서화: 수집·분석된 모든 데이터를 종합하여 맞춤형 진출 전략 보고서를 자동 작성(PDF/문서화)하여 의사결정에 바로 활용할 수 있도록 제공합니다.


## Tech Stack 

| Category   | Details                      |
|------------|------------------------------|
| Framework  | LangGraph, LangChain, Python |
| LLM        | GPT-4o-mini via OpenAI API   |
| Retrieval  | FAISS, Chroma                |


## Agents
 
- 시장 분석 Agent: 9개국(Stanford AI index 기준 ai 산업 성장성이 높은 10개국 중 한국 제외)의 AI 산업과 관련한 시장 동향 정보 수집, PESTEL 분석. 
- 기업 Agent: 대상 기업 정보 수집, 강점/약점 분석.
- 진출 지역 선정 Agent: 상기 두 Agent의 결과를 바탕으로 기업에게 가장 적합한 진출 국가를 정량적 평가 및 우선 순위로 선정
- 경쟁 분석 Agent: 선정된 진출 지역 내 경쟁 상황 정보 수집
- 파트너 분석 Agent: 선정된 진출 지역 내 파트너 후보 정보 수집 
- 전략 보고서 작성 Agent: 전체 분석 결과와 전략적 인사이트를 종합하여, 맞춤형 진출 전략 보고서 작성·정리

## State 
    market: Annotated[Sequence[BaseMessage], add_messages]
    company: Annotated[Sequence[BaseMessage], add_messages]
    selected_country: Annotated[Sequence[BaseMessage], add_messages]
    competitors: Annotated[Sequence[BaseMessage], add_messages]
    partners: Annotated[Sequence[BaseMessage], add_messages]
    report: Annotated[Sequence[BaseMessage], add_messages]


## Architecture
![graphdiagram](./graphdiagram.PNG)

## Directory Structure
├── data/                  # 스타트업 PDF 문서
├── agents/                # 평가 기준별 Agent 모듈
├── prompts/               # 프롬프트 템플릿
├── outputs/               # 평가 결과 저장
├── app.py                 # 실행 스크립트
└── README.md

## Contributors 
- 정선웅 : Prompt Engineering, Agent Design 
