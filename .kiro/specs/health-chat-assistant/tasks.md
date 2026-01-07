# Implementation Plan: Health Chat Assistant

## Overview

This implementation plan breaks down the Health Chat Assistant into discrete coding tasks. The approach follows a bottom-up strategy: first implementing data models and core infrastructure, then building the service layer components, followed by LLM integration, and finally the API endpoints with streaming support.

## Tasks

- [ ] 1. Set up data models and database schema
  - Create Pydantic models for ChatSession, Message, ChatContext, ResearchResults
  - Define database tables for chat sessions and messages
  - Set up Alembic migration for new tables
  - Create enums for MessageRole, StreamEventType
  - _Requirements: 1.1, 1.2, 4.1, 4.2, 6.1_

- [ ]* 1.1 Write property test for data model completeness
  - **Property 16: Session Summary Completeness**
  - **Validates: Requirements 4.5**

- [ ] 2. Implement Message Store service
  - [ ] 2.1 Create MessageStore class with persistence methods
    - Implement save_message method
    - Implement get_messages with pagination
    - Implement delete_session_messages for cascade deletion
    - Implement update_message for partial responses
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ]* 2.2 Write property tests for message persistence
    - **Property 12: Message Persistence**
    - **Property 13: Complete History Retrieval**
    - **Property 14: Chronological Message Ordering**
    - **Validates: Requirements 4.1, 4.2, 4.3**

  - [ ]* 2.3 Write unit tests for message store
    - Test message saving and retrieval
    - Test pagination
    - Test cascade deletion
    - Test update operations
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 3. Implement Session Manager service
  - [ ] 3.1 Create SessionManager class
    - Implement create_session method
    - Implement get_session method
    - Implement update_session_activity method
    - Implement archive_inactive_sessions method
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]* 3.2 Write property tests for session management
    - **Property 21: Unique Session Identifiers**
    - **Property 22: Session Ordering by Activity**
    - **Property 23: Automatic Archiving**
    - **Property 15: Cascade Deletion**
    - **Validates: Requirements 6.1, 6.2, 6.5, 4.4, 6.4**

  - [ ]* 3.3 Write unit tests for session manager
    - Test session creation with unique IDs
    - Test session retrieval
    - Test activity updates
    - Test archiving logic
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [ ] 4. Checkpoint - Ensure data layer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Context Builder service
  - [ ] 5.1 Create ContextBuilder class
    - Implement build_context method
    - Implement get_relevant_biomarkers method
    - Implement get_relevant_documents method
    - Implement summarize_conversation_history method
    - _Requirements: 1.2, 1.4, 2.1, 2.2, 2.3, 2.4, 11.1, 11.2, 11.3_

  - [ ]* 5.2 Write property tests for context building
    - **Property 2: Conversation History Maintenance**
    - **Property 3: Context Summarization on Overflow**
    - **Property 4: Digital Twin Context Inclusion**
    - **Property 35: Document Context Inclusion**
    - **Validates: Requirements 1.2, 1.4, 2.1, 11.1**

  - [ ]* 5.3 Write unit tests for context builder
    - Test context building with complete data
    - Test with missing digital twin data
    - Test conversation summarization
    - Test document retrieval
    - _Requirements: 1.2, 1.4, 2.1, 2.4, 11.1_

- [ ] 6. Implement Prompt Builder service
  - [ ] 6.1 Create PromptBuilder class
    - Implement build_system_prompt method
    - Implement build_user_prompt method
    - Implement get_safety_guidelines method
    - Implement format_digital_twin_context method
    - _Requirements: 2.1, 2.5, 8.1, 8.2, 8.3, 8.4, 9.4_

  - [ ]* 6.2 Write property tests for safety guidelines
    - **Property 24: Medical Disclaimer Inclusion**
    - **Property 25: Emergency Symptom Response**
    - **Property 26: Diagnosis Refusal**
    - **Property 27: Medication Change Warning**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**

  - [ ]* 6.3 Write property test for biomarker formatting
    - **Property 5: Biomarker Value Citation**
    - **Property 29: Units and Reference Ranges**
    - **Validates: Requirements 2.2, 2.5, 9.4**

  - [ ]* 6.4 Write unit tests for prompt builder
    - Test system prompt generation
    - Test safety guidelines inclusion
    - Test digital twin formatting
    - _Requirements: 2.1, 8.1_

- [ ] 7. Implement Research Agent service
  - [ ] 7.1 Create ResearchAgent class
    - Implement research method
    - Implement search_medical_knowledge method
    - Implement synthesize_sources method
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

  - [ ]* 7.2 Write property tests for research
    - **Property 17: Research Triggering**
    - **Property 18: Source Citation**
    - **Property 19: Research Indication**
    - **Property 20: Research Failure Handling**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.5**

  - [ ]* 7.3 Write unit tests for research agent
    - Test research with successful results
    - Test research with no results
    - Test research failures
    - Test source synthesis
    - _Requirements: 5.1, 5.2, 5.5_

- [ ] 8. Checkpoint - Ensure service layer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement Stream Handler service
  - [ ] 9.1 Create StreamHandler class
    - Implement stream_response method for SSE
    - Implement format_sse_message method
    - Implement handle_stream_error method
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 9.2 Write property tests for streaming
    - **Property 8: Streaming Token Delivery**
    - **Property 9: Stream Completion Signal**
    - **Property 10: Graceful Stream Error Handling**
    - **Property 11: Cancellation Handling**
    - **Validates: Requirements 3.1, 3.3, 3.4, 3.5**

  - [ ]* 9.3 Write unit tests for stream handler
    - Test SSE message formatting
    - Test stream completion
    - Test error handling
    - Test cancellation
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 10. Implement LLM Orchestrator service
  - [ ] 10.1 Create LLMOrchestrator class
    - Implement generate_response method with streaming
    - Implement generate_with_research method
    - Implement should_perform_research method
    - Add retry logic with exponential backoff
    - _Requirements: 1.1, 5.1, 9.1, 12.1, 12.2_

  - [ ]* 10.2 Write property tests for LLM orchestration
    - **Property 1: Response Generation for All Messages**
    - **Property 28: Model Version Tracking**
    - **Property 40: LLM Request Retry Logic**
    - **Property 41: Retry Exhaustion Error Message**
    - **Validates: Requirements 1.1, 9.1, 12.1, 12.2**

  - [ ]* 10.3 Write unit tests for LLM orchestrator
    - Test response generation
    - Test research triggering
    - Test retry logic
    - Test error handling
    - _Requirements: 1.1, 5.1, 12.1, 12.2_

- [ ] 11. Implement main Chat Service orchestrator
  - [ ] 11.1 Create ChatService class
    - Implement send_message method with streaming
    - Implement create_session method
    - Implement get_session method
    - Implement list_sessions method
    - Implement delete_session method
    - Wire together all service components
    - _Requirements: 1.1, 1.2, 4.1, 4.2, 6.1, 6.2, 6.3, 6.4_

  - [ ]* 11.2 Write property tests for chat service
    - **Property 6: Medical Condition Awareness**
    - **Property 7: Missing Data Acknowledgment**
    - **Property 36: Document Biomarker Extraction**
    - **Property 37: Document Relevance Selection**
    - **Validates: Requirements 2.3, 2.4, 11.2, 11.3**

  - [ ]* 11.3 Write integration tests for chat service
    - Test complete conversation flow
    - Test session management
    - Test context integration
    - Test error recovery
    - _Requirements: 1.1, 1.2, 4.1, 6.1_

- [ ] 12. Checkpoint - Ensure all service integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Implement caching layer
  - [ ] 13.1 Add Redis caching for digital twin data
    - Implement cache get/set for digital twin data
    - Add cache invalidation logic
    - Implement fallback to database on cache miss
    - _Requirements: 10.4, 12.3_

  - [ ]* 13.2 Write property tests for caching
    - **Property 33: Digital Twin Data Caching**
    - **Property 42: Digital Twin Fallback**
    - **Validates: Requirements 10.4, 12.3**

- [ ] 14. Implement performance and load handling
  - [ ] 14.1 Add performance optimizations
    - Implement context window size reduction under load
    - Add request queueing with position feedback
    - Implement rate limiting per user
    - _Requirements: 10.1, 10.2, 10.3, 10.5_

  - [ ]* 14.2 Write property tests for performance
    - **Property 30: First Token Response Time**
    - **Property 31: Queue Position Feedback**
    - **Property 32: Graceful Degradation Under Load**
    - **Property 34: Rate Limit Communication**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.5**

- [ ] 15. Implement document integration
  - [ ] 15.1 Add document reference handling
    - Implement document retrieval by reference
    - Add biomarker extraction from documents
    - Implement document summarization
    - Add missing document handling
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ]* 15.2 Write property tests for document handling
    - **Property 38: Document Summarization**
    - **Property 39: Missing Document Handling**
    - **Validates: Requirements 11.4, 11.5**

- [ ] 16. Implement error handling and recovery
  - [ ] 16.1 Add comprehensive error handling
    - Implement error response formatting
    - Add graceful degradation logic
    - Implement message save failure handling
    - Add seamless error recovery
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

  - [ ]* 16.2 Write property tests for error handling
    - **Property 43: Message Save Failure Handling**
    - **Property 44: Seamless Error Recovery**
    - **Validates: Requirements 12.4, 12.5**

- [ ] 17. Checkpoint - Ensure all core functionality tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 18. Create API endpoints
  - [ ] 18.1 Add FastAPI chat endpoints
    - POST /api/chat/sessions - Create new session
    - GET /api/chat/sessions - List user sessions
    - GET /api/chat/sessions/{session_id} - Get session with messages
    - DELETE /api/chat/sessions/{session_id} - Delete session
    - POST /api/chat/sessions/{session_id}/messages - Send message (SSE streaming)
    - Add authentication middleware
    - _Requirements: 1.1, 4.1, 4.2, 6.1, 6.2, 6.3, 6.4_

  - [ ] 18.2 Implement SSE streaming endpoint
    - Configure SSE response headers
    - Wire StreamHandler to endpoint
    - Add connection management
    - _Requirements: 3.1, 3.2, 3.4_

  - [ ]* 18.3 Write API integration tests
    - Test session creation endpoint
    - Test message sending with streaming
    - Test session listing and retrieval
    - Test session deletion
    - Test authentication
    - _Requirements: 1.1, 3.1, 4.1, 6.1, 6.2, 6.3, 6.4_

- [ ] 19. Add API documentation
  - [ ] 19.1 Create OpenAPI documentation
    - Document all endpoints with examples
    - Add request/response schemas
    - Include SSE streaming documentation
    - Add authentication requirements
    - _Requirements: All_

- [ ] 20. Implement LLM provider integration
  - [ ] 20.1 Add LLM provider client
    - Implement OpenAI API client (or chosen provider)
    - Add streaming support
    - Implement retry logic
    - Add error handling
    - _Requirements: 1.1, 3.1, 9.1, 12.1_

  - [ ]* 20.2 Write integration tests for LLM provider
    - Test successful response generation
    - Test streaming
    - Test error handling
    - Test retry logic
    - _Requirements: 1.1, 3.1, 12.1_

- [ ] 21. Add monitoring and logging
  - [ ] 21.1 Implement logging infrastructure
    - Add structured logging for all services
    - Log LLM requests and responses
    - Log errors and retries
    - Add performance metrics logging
    - _Requirements: 9.1, 10.1, 12.1_

  - [ ] 21.2 Add monitoring hooks
    - Track response times
    - Monitor error rates
    - Track cache hit rates
    - Monitor LLM API usage
    - _Requirements: 10.1, 10.4_

- [ ] 22. Final checkpoint - End-to-end testing
  - [ ] 22.1 Run full test suite
    - Ensure all property tests pass (100 iterations)
    - Ensure all unit tests pass
    - Ensure all integration tests pass
    - _Requirements: All_

  - [ ] 22.2 Test complete user flows
    - Create session → Send messages → Receive streaming responses
    - Test with real digital twin data
    - Test document references
    - Test research triggering
    - Test error scenarios
    - _Requirements: All_

  - [ ] 22.3 Performance testing
    - Test first token latency
    - Test concurrent users
    - Test cache performance
    - Test under load
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using Hypothesis
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end flows
- The implementation uses Python with FastAPI, matching the existing backend stack
- LLM provider can be OpenAI, Anthropic, or any compatible API
- SSE (Server-Sent Events) is used for streaming responses to maintain HTTP compatibility
