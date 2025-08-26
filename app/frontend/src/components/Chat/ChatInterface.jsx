import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import MessageInput from './MessageInput';
import { chatAPI } from '../../services/api';

// Mock responses for demo (same as in original HTML)
const fakeResponses = {
  'điều kiện cho vay thế chấp là gì?': `
    <div class="answer-card">
      <div class="answer-header">
        <strong>Trả lời chính</strong>
        <span class="status-badge valid"><i class="fas fa-check-circle"></i> Còn hiệu lực</span>
      </div>
      <div class="answer-body">
        Tổ chức tín dụng (TCTD) xem xét và quyết định cho vay khi khách hàng có đủ các điều kiện sau:
        <ol>
          <li><b>Năng lực pháp luật và hành vi dân sự:</b> Khách hàng là pháp nhân hoặc cá nhân từ đủ 18 tuổi trở lên.</li>
          <li><b>Mục đích vay vốn hợp pháp.</b></li>
          <li><b>Phương án sử dụng vốn khả thi.</b></li>
          <li><b>Khả năng tài chính để trả nợ.</b></li>
          <li><b>Có tài sản bảo đảm (TSĐB)</b> cho khoản vay theo quy định của TCTD và pháp luật.</li>
        </ol>
      </div>
      <div class="answer-citations">
        <div class="citation-item">
          <span class="source"><a href="#" target="_blank">Điều 7, Thông tư 39/2016/TT-NHNN</a></span>
        </div>
      </div>
    </div>
  `,
  'tạo checklist mở thẻ tín dụng': `
    <div class="answer-card">
      <div class="answer-header">
        <strong>Checklist: Mở Thẻ Tín Dụng</strong>
        <span class="status-badge valid"><i class="fas fa-check-circle"></i> Còn hiệu lực</span>
      </div>
      <div class="answer-body checklist">
        Dưới đây là danh mục hành động tuân thủ tự động cho quy trình phát hành thẻ tín dụng:
        <ul>
          <li>Nhận diện và xác minh thông tin khách hàng (KYC).</li>
          <li>Yêu cầu khách hàng điền vào giấy đề nghị phát hành thẻ theo mẫu của TCTD.</li>
          <li>Thu thập và thẩm định hồ sơ chứng minh nhân thân (CCCD/Hộ chiếu).</li>
          <li>Thu thập và thẩm định hồ sơ chứng minh khả năng tài chính (HĐLĐ, sao kê lương).</li>
          <li>Kiểm tra lịch sử tín dụng của khách hàng trên CIC.</li>
          <li>Ký kết hợp đồng phát hành và sử dụng thẻ với khách hàng.</li>
        </ul>
      </div>
    </div>
  `,
  'so sánh nghị định 10/2023 và 99/2022 về đăng ký tsđb': `
    <div class="answer-card">
      <div class="answer-header">
        <strong>Diff & Redline: Đăng ký Tài sản bảo đảm</strong>
        <span class="status-badge valid"><i class="fas fa-info-circle"></i> Phân tích thay đổi</span>
      </div>
      <div class="answer-body">
        Nghị định 10/2023/NĐ-CP đã sửa đổi một số quy định trong Nghị định 99/2022/NĐ-CP, đáng chú ý là về việc cấp bản sao văn bản chứng nhận đăng ký biện pháp bảo đảm.
      </div>
      <div class="answer-citations">
        <div class="citation-item">
          <span class="source"><a href="#" target="_blank">Khoản 5, Điều 1, Nghị định 10/2023/NĐ-CP</a></span>
        </div>
      </div>
    </div>
  `,
};

const noAnswerResponse = `
  <div class="answer-card">
    <div class="answer-header">
      <strong>Không thể trả lời</strong>
      <span class="status-badge warning"><i class="fas fa-exclamation-triangle"></i> No Citation, No Answer</span>
    </div>
    <div class="answer-body">
      Để đảm bảo tính chính xác và giảm thiểu "ảo giác" (hallucination), tôi không thể cung cấp câu trả lời do không truy hồi được trích dẫn pháp lý đáng tin cậy từ cơ sở tri thức hiện tại.
      <br><br>
      Vui lòng thử diễn đạt lại câu hỏi hoặc tải lên tài liệu liên quan để tôi phân tích.
    </div>
  </div>
`;

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage = {
      id: Date.now(),
      message: `<strong>Xin chào!</strong> Tôi là trợ lý pháp lý URA-xLaw. Tôi có thể giúp bạn tra cứu, so sánh, và tạo checklist tuân thủ từ các văn bản pháp luật ngân hàng.
      <br><br>Bạn có thể thử các câu hỏi sau:
      <ul>
        <li><code>Điều kiện cho vay thế chấp là gì?</code></li>
        <li><code>Tạo checklist tuân thủ cho việc mở thẻ tín dụng</code></li>
        <li><code>So sánh Nghị định 10/2023 và 99/2022 về đăng ký tsđb</code></li>
      </ul>`,
      type: 'bot',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      message: message,
      type: 'user',
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Try to call the real API first
      try {
        const response = await chatAPI.sendMessage(message);
        const botMessage = {
          id: Date.now() + 1,
          message: response.message,
          type: 'bot',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, botMessage]);
      } catch (error) {
        console.log('API not available, using mock response:', error.message);
        
        // Use mock response as fallback
        const mockResponse = fakeResponses[message.toLowerCase()] || noAnswerResponse;
        
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const botMessage = {
          id: Date.now() + 1,
          message: mockResponse,
          type: 'bot',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        message: 'Đã xảy ra lỗi khi xử lý tin nhắn. Vui lòng thử lại.',
        type: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="chat" aria-live="polite">
      <div className="chat-header">
        <div>
          <div style={{ fontSize: '13px', color: 'var(--muted)' }}>Trò chuyện với</div>
          <div className="title">Trợ lý Pháp lý URA</div>
        </div>
        <div className="meta">Model: URA-Agent-v2.1 • KB cập nhật: 09/08/2025</div>
      </div>

      <div className="messages" tabindex="0" role="log" aria-label="Tin nhắn">
        {messages.map((msg) => (
          <Message
            key={msg.id}
            message={msg.message}
            type={msg.type}
            timestamp={msg.timestamp}
          />
        ))}
        {isLoading && (
          <div className="msg bot">
            <i className="fas fa-spinner spinner"></i> URA đang áp dụng các agent (Retriever, Applicability, Citation...) để xử lý...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </main>
  );
};

export default ChatInterface;
