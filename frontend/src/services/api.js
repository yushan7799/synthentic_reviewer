const API_BASE_URL = '/api';

class APIService {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Panelist endpoints
    async getPanelists() {
        return this.request('/panelists');
    }

    async getPanelist(id) {
        return this.request(`/panelists/${id}`);
    }

    async createPanelist(data) {
        return this.request('/panelists', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updatePanelist(id, data) {
        return this.request(`/panelists/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deletePanelist(id) {
        return this.request(`/panelists/${id}`, {
            method: 'DELETE',
        });
    }

    // Proposal endpoints
    async getProposals() {
        return this.request('/proposals');
    }

    async getProposal(id) {
        return this.request(`/proposals/${id}`);
    }

    async uploadProposal(file) {
        const formData = new FormData();
        formData.append('file', file);

        return fetch(`${API_BASE_URL}/proposals/upload`, {
            method: 'POST',
            body: formData,
        }).then(res => res.json());
    }

    async deleteProposal(id) {
        return this.request(`/proposals/${id}`, {
            method: 'DELETE',
        });
    }

    // Review endpoints
    async generateReview(panelistId, proposalId) {
        return this.request('/reviews/generate', {
            method: 'POST',
            body: JSON.stringify({
                panelist_id: panelistId,
                proposal_id: proposalId,
            }),
        });
    }

    async generatePanelReview(proposalId, panelistIds = null) {
        return this.request('/reviews/panel', {
            method: 'POST',
            body: JSON.stringify({
                proposal_id: proposalId,
                panelist_ids: panelistIds,
            }),
        });
    }

    async getProposalReviews(proposalId) {
        return this.request(`/reviews/proposal/${proposalId}`);
    }

    async submitReviewFeedback(reviewId, rating, feedback) {
        return this.request(`/reviews/${reviewId}/feedback`, {
            method: 'POST',
            body: JSON.stringify({ rating, feedback }),
        });
    }

    // Utility endpoints
    async extractProfile(url) {
        return this.request('/extract-profile', {
            method: 'POST',
            body: JSON.stringify({ url }),
        });
    }

    async healthCheck() {
        return this.request('/health');
    }
}

export default new APIService();
