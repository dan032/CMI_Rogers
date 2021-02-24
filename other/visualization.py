import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("outputs/output7.csv")
df1 = df[df.protocols.str.contains('s1ap')]
df2 = df[df.protocols.str.contains('gtp')]
plt.hist(df1.enb_ue_s1ap_id, bins=20)
plt.ylabel("Count")
plt.xlabel("eNB UE S1AP ID")
plt.show()

plt.hist(df1.mme_ue_s1ap_id, bins=20)
plt.ylabel("Count")
plt.xlabel("MME UE S1AP ID")
plt.show()

# plt.hist(df.gtp_teid, bins=20)
# plt.ylabel("Count")
# plt.xlabel("GTP TEID")
# plt.show()

plt.hist(df1.cellidentity, bins=20)
plt.ylabel("Count")
plt.xlabel("Cell Identity")
plt.show()

# plt.hist(df1.nas_eps_bearer_id, bins=20)
# plt.ylabel("Count")
# plt.xlabel("NAS EPS Bearer ID")
# plt.show()

plt.hist(df2.teid, bins=20)
plt.ylabel("Count")
plt.xlabel("TEID")
plt.show()