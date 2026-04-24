from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from .rag import InMemoryLegalRAG


app = FastAPI(
    title="Legal Advisor API",
    version="1.0.0",
    description="AI-powered legal consultation API with retrieval-augmented generation"
)

# Enable CORS for all origins (configure as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = InMemoryLegalRAG()


# Sample legal documents to auto-load on startup
SAMPLE_DOCUMENTS = {
    "us-contract-law": """CONTRACT LAW FUNDAMENTALS - UNITED STATES

A contract is a legally binding agreement between two or more parties that creates obligations enforceable by law. The essential elements of a valid contract are: (1) Offer - one party proposes terms to another party; (2) Acceptance - the other party agrees to the exact terms of the offer; (3) Consideration - something of value exchanged between parties; (4) Mutual Intent - both parties intend to be legally bound; (5) Capacity - both parties have legal ability to contract; (6) Legality - the purpose of the contract is legal.

OFFER: An offer is a manifestation of willingness to enter into an agreement, made in such a way that another person is justified in understanding that his assent to that manifestation is invited and will conclude the contract. The offer must be definite, communicated, and show intent to be bound. Under the Uniform Commercial Code (UCC), an offer to buy or sell goods may be made in any manner sufficient to show agreement. An offer can be revoked by the offeror at any time before acceptance unless it is an option contract.

ACCEPTANCE: Acceptance is a manifestation of assent to the terms of an offer made by the offeree in a manner invited or required by the offer. Once a valid acceptance occurs, a binding contract is formed. Generally, acceptance must be communicated to the offeror. The "mailbox rule" states that acceptance is effective when sent, not when received. However, revocations are effective only when received.

CONSIDERATION: Consideration is a bargained-for exchange of value between the parties. Both parties must give something up or both must gain something. Consideration can be money, goods, services, or a promise to do or not do something. Past consideration generally is not valid consideration. Courts will not usually evaluate whether the consideration is fair or adequate.

CAPACITY: Both parties must have legal capacity to contract. This means they must be of legal age, mentally competent, and not under the influence. Minors generally can void contracts. Those adjudged mentally incompetent cannot form valid contracts. Intoxicated persons may lack capacity depending on severity of intoxication.

LEGALITY: The purpose and performance of a contract must be legal. Contracts with illegal purposes are void and unenforceable. Examples include contracts for illegal services, gambling contracts (in most states), and agreements restraining trade beyond reasonable limits.""",

    "us-employment-law": """EMPLOYMENT LAW OVERVIEW - UNITED STATES

EMPLOYMENT AT-WILL: Employment at will is the default rule in the United States. Under this doctrine, an employer can terminate an employee for any reason or no reason at all, and an employee can quit for any reason, unless otherwise specified in an employment contract. However, there are important limitations to the at-will doctrine.

WRONGFUL TERMINATION: An employee cannot be fired for illegal reasons. Wrongful termination occurs when an employee is fired in violation of public policy or employment laws. Examples include firing for: refusing to commit an illegal act, reporting illegal activity (whistleblower protection), filing a workers' compensation claim, exercising legal rights, or discriminatory reasons.

DISCRIMINATION: Federal law prohibits discrimination based on race, color, religion, sex, national origin, age (40+), disability, or genetic information. Title VII of the Civil Rights Act applies to employers with 15+ employees. The Age Discrimination in Employment Act (ADEA) applies to employers with 20+ employees. The Americans with Disabilities Act (ADA) requires reasonable accommodations for qualified individuals with disabilities.

HARASSMENT: Workplace harassment includes unwelcome conduct based on protected characteristics that is severe or pervasive enough to create a hostile work environment. Sexual harassment includes unwelcome sexual advances, requests for sexual favors, and other verbal or physical harassment of a sexual nature. Employers are liable for harassment by supervisors and, in some cases, by coworkers or third parties.

WAGE AND HOUR: The Fair Labor Standards Act (FLSA) establishes minimum wage, overtime, and record-keeping requirements. As of 2024, the federal minimum wage is $7.25 per hour. Non-exempt employees must be paid overtime at 1.5 times their regular rate for hours worked over 40 per week. Employers must maintain accurate records of hours worked and wages paid.

FAMILY AND MEDICAL LEAVE: The Family and Medical Leave Act (FMLA) requires employers with 50+ employees to provide up to 12 weeks of unpaid leave for qualifying events: birth or adoption of a child, care for a family member with serious health condition, or employee's own serious health condition. The employee must be restored to the same position or equivalent position.""",

    "us-property-law": """PROPERTY LAW ESSENTIALS - UNITED STATES

REAL PROPERTY: Real property includes land and things permanently attached to land (buildings, trees). Real property rights include possession, use, transfer, and enjoyment. Real property is transferred by deed, which must be in writing and properly executed to be valid.

PERSONAL PROPERTY: Personal property is movable property, including tangible items (cars, furniture) and intangible items (stocks, patents). Personal property transfers can be made orally, in writing, or by delivery. Bailment is the delivery of personal property to another person for a particular purpose.

LANDLORD AND TENANT: A landlord-tenant relationship creates when a property owner (landlord) leases property to another person (tenant) for a specified period. The landlord must provide premises that comply with building codes and are fit for the purpose intended. The tenant must pay rent as agreed and maintain the premises in reasonable condition.

EVICTION: Eviction is the legal process to remove a tenant from property. The landlord must follow proper legal procedures, including providing notice (usually 30-60 days) and filing in court. Eviction for non-payment of rent, material breach of lease, or lease expiration are common reasons. Illegal self-help eviction is prohibited in all states.

TITLE AND OWNERSHIP: Title is the legal ownership of property. Title can be held individually, jointly (with right of survivorship), in tenancy in common, or in a trust. Adverse possession allows a person to gain title to property by openly occupying it for a statutory period (typically 7-21 years depending on the state) with the intent to claim ownership.

EASEMENTS AND COVENANTS: An easement is the right to use another's property for a specific purpose (e.g., utility easement). Covenants are restrictions on how property can be used. Easements and covenants run with the land and bind future owners. They are enforced through injunctions or damage awards.""",

    "us-criminal-procedure": """CRIMINAL PROCEDURE - UNITED STATES

ARREST AND DETENTION: Police may arrest a person with a warrant based on probable cause or may make a warrantless arrest if they have probable cause to believe a crime has been committed. Once arrested, a person must be informed of their rights (Miranda rights) before custodial interrogation. The person has the right to remain silent, the right to an attorney, and the right to have an attorney appointed if they cannot afford one.

SEARCHES AND SEIZURES: The Fourth Amendment protects against unreasonable searches and seizures. Generally, police need a warrant based on probable cause to search a person or their property. A warrant must specifically describe the place to be searched and the items to be seized. Exceptions to the warrant requirement include: consent, plain view, exigent circumstances, and incident to a lawful arrest.

MIRANDA RIGHTS: Miranda rights must be given before custodial interrogation. The person must be told: (1) You have the right to remain silent; (2) Anything you say can be used against you in court; (3) You have the right to an attorney; (4) If you cannot afford an attorney, one will be appointed. Failure to read Miranda rights does not make the arrest illegal but makes statements inadmissible.

INDICTMENT AND CHARGES: A person charged with a felony generally has the right to a grand jury indictment. The prosecution must prove probable cause to the grand jury. The defendant has the right to be informed of the charges and the evidence. Discovery rights allow the defendant to see evidence held by the prosecution.

TRIAL RIGHTS: The defendant has the right to: a speedy trial, an impartial jury, confront witnesses, present a defense, and counsel. The prosecution must prove guilt beyond a reasonable doubt. Double jeopardy protections prevent the government from trying someone twice for the same crime.

SENTENCING: After conviction, the court imposes a sentence. Sentencing factors include criminal history, nature of the offense, and victim impact. Many crimes have mandatory minimum sentences. Appeals can challenge conviction on legal grounds or claim ineffective assistance of counsel.""",

    "contract-templates": """SAMPLE CONTRACT CLAUSES AND PROVISIONS

PAYMENT TERMS: Payment shall be made within thirty (30) days of invoice date. If payment is not received by the due date, a late fee of 1.5% per month shall be assessed on the outstanding balance. Payment should be made to [Payee Address].

TERM AND TERMINATION: This Agreement shall commence on [Start Date] and continue for a period of [Duration], unless earlier terminated. Either party may terminate this Agreement with thirty (30) days written notice to the other party. Upon termination, all obligations shall cease except those that by their nature are intended to survive termination.

CONFIDENTIALITY: The parties agree to maintain the confidentiality of all proprietary and confidential information disclosed under this Agreement. Confidential information shall not be disclosed to third parties without prior written consent. This obligation shall survive termination of this Agreement for a period of [Duration].

WARRANTIES AND DISCLAIMERS: [Service Provider] warrants that the services will be performed in a professional and workmanlike manner. EXCEPT AS EXPRESSLY SET FORTH HEREIN, [SERVICE PROVIDER] MAKES NO OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING ANY WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

LIMITATION OF LIABILITY: Neither party shall be liable for indirect, incidental, consequential, or special damages, including lost profits, even if advised of the possibility of such damages. Each party's total liability shall not exceed the fees paid by [Client] under this Agreement in the twelve (12) months preceding the claim.

INDEMNIFICATION: [Service Provider] shall indemnify, defend, and hold harmless [Client] from any claims, damages, and costs arising from [Service Provider]'s breach of this Agreement or violation of applicable law.""",
}


@app.on_event("startup")
async def startup_event():
    """Auto-load sample legal documents on startup"""
    print("[INFO] Loading sample legal documents...")
    for doc_id, text in SAMPLE_DOCUMENTS.items():
        try:
            rag.ingest(doc_id, text)
            print(f"✓ Loaded {doc_id}")
        except Exception as e:
            print(f"✗ Failed to load {doc_id}: {e}")
    stats = rag.get_stats()
    print(f"[INFO] RAG System Ready: {stats['total_chunks']} chunks indexed")


class IngestRequest(BaseModel):
    doc_id: str = Field(..., description="Unique document identifier", min_length=1, max_length=255)
    text: str = Field(..., description="Full legal text", min_length=10, max_length=1_000_000)

    @validator("doc_id")
    def validate_doc_id(cls, v):
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("doc_id must be alphanumeric with hyphens or underscores")
        return v


class Citation(BaseModel):
    doc_id: str
    chunk_id: int
    score: float


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    jurisdiction: str = Field(default="US", min_length=2, max_length=50)
    practice_area: str = Field(default="general", min_length=1, max_length=50)

    @validator("message")
    def validate_message(cls, v):
        if len(v.strip()) == 0:
            raise ValueError("Message cannot be empty or whitespace-only")
        return v.strip()


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    disclaimer: str


@app.get("/health", tags=["Health"])
def health() -> dict:
    """Health check endpoint"""
    stats = rag.get_stats()
    return {"status": "ok", "version": "1.0.0", "chunks_indexed": stats["total_chunks"]}


@app.post("/ingest", response_model=dict, tags=["Documents"])
def ingest(payload: IngestRequest) -> dict:
    """
    Ingest a legal document for RAG retrieval.
    
    Args:
        payload: Document to ingest (doc_id and text)
    
    Returns:
        Status and number of chunks created
    """
    try:
        count = rag.ingest(payload.doc_id, payload.text)
        return {
            "status": "indexed",
            "chunks": count,
            "doc_id": payload.doc_id,
            "message": f"Successfully indexed {count} chunks"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(payload: ChatRequest) -> ChatResponse:
    """
    Chat with the legal advisor AI.
    
    Args:
        payload: Chat request with message, jurisdiction, and practice area
    
    Returns:
        ChatResponse with answer, citations, and disclaimer
    """
    try:
        # Retrieve relevant legal documents
        hits = rag.retrieve(payload.message, top_k=3)
        citations = [
            Citation(doc_id=h["doc_id"], chunk_id=h["chunk_id"], score=h["score"])
            for h in hits
        ]

        # Generate answer based on retrieved documents
        if not hits:
            answer = (
                "I could not find grounded legal text for this question. "
                f"The system currently has legal information about: Contract Law, Employment Law, Property Law, Criminal Procedure, and Contract Templates. "
                f"Please try asking about these topics, or ingest additional documents. "
                f"(Jurisdiction: {payload.jurisdiction}, Practice Area: {payload.practice_area})"
            )
        else:
            snippets = "\n\n".join(
                f"[{i+1}] From {h['doc_id']} (Match: {h['score']:.0%}):\n{h['text'][:300]}..."
                for i, h in enumerate(hits)
            )
            answer = (
                f"Based on retrieved legal sources for {payload.jurisdiction} law in {payload.practice_area}:\n\n"
                f"{snippets}\n\n"
                "For a comprehensive answer, please review the full documents above or consult a qualified attorney."
            )

        return ChatResponse(
            answer=answer,
            citations=citations,
            disclaimer=(
                "DISCLAIMER: This assistant provides general legal information only, not legal advice. "
                "The responses are based on ingested documents and should not be relied upon for legal decisions. "
                "Always consult a licensed attorney in your jurisdiction for advice specific to your situation."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat request failed: {str(e)}")


@app.get("/stats", tags=["Admin"])
def get_stats() -> dict:
    """Get RAG system statistics"""
    stats = rag.get_stats()
    return {
        "total_chunks": stats["total_chunks"],
        "indexed": stats["is_indexed"],
        "unique_docs": stats["unique_docs"],
        "message": "System is ready for queries"
    }

