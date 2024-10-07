from rest_framework import serializers
from templates import models


class PaperSerializer(serializers.ModelSerializer):
    extra = serializers.SerializerMethodField()

    class Meta:
        model = models.Paper
        fields = "__all__"
        read_only_fields = ["fiscal_year"]

    def _get_documents(self, obj):
        qs = obj.documents.all()
        serializer = PaperDocumentSerializer(qs, many=True, context=self.context)
        return serializer.data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["documents"] = self._get_documents(instance)
        return data

    def validate(self, attrs):
        status = attrs.get("status")
        remarks = attrs.get("remarks")
        if status == "Rejected" and not remarks:
            raise serializers.ValidationError("remarks is required for rejected paper")
        return attrs


class PaperDetailSerializer(PaperSerializer):
    remarks = serializers.SerializerMethodField()
    settlement_remarks = serializers.SerializerMethodField()

    def get_settlement_remarks(self, obj):
        if not obj.remarks:
            return None
        data = {"remarks": obj.remarks}
        if obj.settlement_branch:
            data["id"] = obj.settlement_branch.id
            data["fullname_np"] = obj.settlement_branch.fullname_np
            data["fullname_en"] = obj.settlement_branch.fullname_en
        return data

    def get_remarks(self, obj):
        qs = obj.forwared.exclude(remarks="").exclude(remarks=None)
        fields = (
            "forwarder_id",
            "forwarder__fullname_en",
            "forwarder__fullname_np",
            "receiver_id",
            "receiver__fullname_en",
            "receiver__fullname_np",
            "roll_number",
            "remarks",
            "images",
            "created_at",
        )
        data = qs.values(*fields)
        return data


class PaperDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaperDocument
        fields = "__all__"


class RelatedBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RelatedBranch
        fields = "__all__"


class FAQSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = "__all__"
