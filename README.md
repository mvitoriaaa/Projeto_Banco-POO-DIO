# # 🏦 Sistema Bancário - Desafio DIO

Implementação orientada a objetos de um sistema bancário simples em Python, baseado no diagrama UML do desafio da [DIO (Digital Innovation One)](https://www.dio.me/).

## 📐 Diagrama de Classes

O sistema foi modelado com as seguintes classes:

```
Transacao (interface)
├── Deposito
└── Saque

Conta
└── ContaCorrente

Cliente
└── PessoaFisica

Historico
```

## 🚀 Como executar

```bash
python sistema_bancario.py
```

## ✨ Funcionalidades

| Opção | Descrição |
|-------|-----------|
| `d`   | Depositar |
| `s`   | Sacar |
| `e`   | Ver extrato |
| `nu`  | Novo usuário |
| `nc`  | Nova conta corrente |
| `lc`  | Listar contas |
| `q`   | Sair |

## 🧱 Estrutura das Classes

### `Transacao` (ABC)
Interface abstrata com o método `registrar(conta)`.

### `Deposito` / `Saque`
Implementam `Transacao`. Registram a operação no histórico da conta.

### `Historico`
Armazena a lista de transações com tipo, valor e data/hora.

### `Conta`
Classe base com saldo, número, agência, cliente e histórico.  
Métodos: `sacar()`, `depositar()`, `nova_conta()`.

### `ContaCorrente`
Herda de `Conta`. Adiciona limite por saque (R$ 500) e limite de saques diários (3).

### `Cliente`
Gerencia a lista de contas e delega transações.  
Métodos: `realizar_transacao()`, `adicionar_conta()`.

### `PessoaFisica`
Herda de `Cliente`. Adiciona CPF, nome e data de nascimento.

## 🔧 Requisitos

- Python 3.10+

## 📁 Estrutura do projeto

```
sistema_bancario/
└── sistema_bancario.py
└── README.md
```

## 👤 Autor

Desenvolvido como parte do bootcamp Python da DIO.
