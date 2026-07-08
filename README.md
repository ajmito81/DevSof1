# DevSof1
content = '''# PLC SKU Router

Sistema ultra-rápido de lookup de SKU para desvio de produtos em tempo real.

**SLA: <20ms por requisição (p99)**

## 📋 Características

- ✅ Socket TCP puro otimizado (<20ms)
- ✅ Cache em memória (HashMap O(1))
- ✅ PostgreSQL com fallback
- ✅ API auxiliar (FastAPI)
- ✅ Monitoramento e métricas
- ✅ Escalável para MQTT/OPC-UA

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
python main.py
```